import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SPEDParser:
    """
    Parser for SPED files (ECF, EFD-Contribuições, EFD ICMS/IPI).
    Detects actual usage of tax incentives and loans recorded in SPED blocks.
    """

    @staticmethod
    def parse_ecf(file_content: str) -> Dict[str, Any]:
        """
        Parses ECF (SPED Contábil/Fiscal) to find LALUR exclusions and Balance Sheet liabilities.
        - Block J: Balanço Patrimonial (debts/loans)
        - Block M/N: e-LALUR/e-LACS (exclusions for Lei do Bem, PAT, SUDENE)
        """
        result = {
            "lei_do_bem_declarado": False,
            "valor_lei_do_bem": 0.0,
            "pat_declarado": False,
            "valor_pat": 0.0,
            "sudene_declarado": False,
            "valor_sudene_beneficio": 0.0,
            "passivos_bancarios": []
        }
        
        if not file_content:
            return result

        lines = file_content.splitlines()
        for line in lines:
            if not line.startswith("|"):
                continue
                
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
                
            reg = parts[1] # e.g. J100, M300, N620
            
            # 1. Lei do Bem in e-LALUR (M300 / M350)
            # Code reference: Exclusão de gastos com P&D (Lei do Bem) - usually code 8, 9 or description in M300
            if reg in ("M300", "M350"):
                desc = parts[3].upper() if len(parts) > 3 else ""
                if "LEI DO BEM" in desc or "P&D" in desc or "PESQUISA DESENVOLVIMENTO" in desc:
                    result["lei_do_bem_declarado"] = True
                    try:
                        val = float(parts[4].replace(",", ".")) if len(parts) > 4 else 0.0
                        result["valor_lei_do_bem"] += val
                    except ValueError:
                        pass

            # 2. PAT in e-LALUR (M300 / M350 / N620)
            if reg in ("M300", "M350", "N620"):
                desc = parts[3].upper() if len(parts) > 3 else ""
                if "PAT " in desc or "ALIMENTACAO TRABALHADOR" in desc or "ALIMENTAÇÃO TRABALHADOR" in desc:
                    result["pat_declarado"] = True
                    try:
                        val = float(parts[4].replace(",", ".")) if len(parts) > 4 else 0.0
                        result["valor_pat"] += val
                    except ValueError:
                        pass
            
            # 3. SUDENE/SUDAM reduction (N620 / N630)
            if reg in ("N620", "N630"):
                desc = parts[3].upper() if len(parts) > 3 else ""
                if "SUDENE" in desc or "SUDAM" in desc or "REDUCAO IRPJ REGIONAL" in desc:
                    result["sudene_declarado"] = True
                    try:
                        val = float(parts[4].replace(",", ".")) if len(parts) > 4 else 0.0
                        result["valor_sudene_beneficio"] += val
                    except ValueError:
                        pass
                        
            # 4. Balanço (J100 / J150) — Passivos de Empréstimos
            if reg == "J100": # Contas do Balanço
                conta_desc = parts[3].upper() if len(parts) > 3 else ""
                if "EMPRESTIMO" in conta_desc or "FINANCIAMENTO" in conta_desc or "DEBENTURE" in conta_desc:
                    try:
                        saldo_final = float(parts[5].replace(",", ".")) if len(parts) > 5 else 0.0
                        if saldo_final > 0:
                            result["passivos_bancarios"].append({
                                "conta": parts[2],
                                "descricao": parts[3],
                                "valor": saldo_final
                            })
                    except ValueError:
                        pass
                        
        return result

    @staticmethod
    def parse_efd_contribuicoes(file_content: str) -> Dict[str, Any]:
        """
        Parses EFD-Contribuições (PIS/COFINS) to find suspension/exemption regimes (PADIS, REIDI, etc.)
        Checks CSTs in A170, C170, F100, etc.
        """
        result = {
            "reidi_declarado": False,
            "padis_declarado": False,
            "reintegra_declarado": False,
            "credito_suspenso": 0.0
        }
        
        if not file_content:
            return result

        lines = file_content.splitlines()
        for line in lines:
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
                
            reg = parts[1]
            
            # In EFD Contribuições, CSTs like 53, 54, 55, 56 represent operations with suspension, isenção or alíquota zero.
            # We look for descriptions or specific indicator registers
            if reg in ("C170", "A170"):
                cst = parts[6] if len(parts) > 6 else "" # CST PIS/COFINS
                if cst in ("53", "54", "55", "56"):
                    desc = parts[3].upper() if len(parts) > 3 else ""
                    if "REIDI" in desc:
                        result["reidi_declarado"] = True
                    elif "PADIS" in desc:
                        result["padis_declarado"] = True
                    elif "REINTEGRA" in desc:
                        result["reintegra_declarado"] = True

        return result

    @staticmethod
    def parse_efd_icms_ipi(file_content: str) -> Dict[str, Any]:
        """
        Parses EFD ICMS/IPI to find presumido credits or ICMS reductions.
        Scans E110/E111 adjustment records.
        """
        result = {
            "credito_presumido_declarado": False,
            "valor_credito_presumido": 0.0,
            "reducao_base_icms": False
        }
        
        if not file_content:
            return result

        lines = file_content.splitlines()
        for line in lines:
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
                
            reg = parts[1]
            if reg == "E111": # Ajustes de Apuração
                codigo_ajuste = parts[2] if len(parts) > 2 else ""
                desc_ajuste = parts[3].upper() if len(parts) > 3 else ""
                
                # Check for standard credit presumido / benefit codes (often starts with UF02, UF04 or contains CRED PRES)
                if "CREDITO PRESUMIDO" in desc_ajuste or "CRED.PRES" in desc_ajuste:
                    result["credito_presumido_declarado"] = True
                    try:
                        val = float(parts[4].replace(",", ".")) if len(parts) > 4 else 0.0
                        result["valor_credito_presumido"] += val
                    except ValueError:
                        pass
                if "REDUCAO BASE" in desc_ajuste or "RED.BASE" in desc_ajuste:
                    result["reducao_base_icms"] = True

        return result
