import asyncio
import logging
from typing import Dict, Any, List

from .bndes_client import BNDESClient
from .finep_client import FINEPClient
from .tax_incentive_client import TaxIncentiveClient
from .gap_analyzer import GapAnalyzer

logger = logging.getLogger(__name__)

DEMO_CNPJ = "29093966000100"

class IncentiveMapper:
    """
    Orchestrator for Módulo 6: Alavancagem Financeira e Mapeamento Global de Incentivos Fiscais.
    Integrates BNDES, FINEP, Tax Incentives and performs Gap Analysis.
    """

    @classmethod
    async def map(
        cls, 
        cnpj: str, 
        cnae: str, 
        regime: str, 
        uf: str, 
        capital_social: float,
        sped_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Maps loans and tax incentives for a given company.
        """
        clean_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")
        
        # 1. Fetch Financing and Loans (BNDES + FINEP)
        loans_task = BNDESClient.search_by_cnpj(clean_cnpj)
        finep_task = FINEPClient.search_by_cnpj(clean_cnpj)
        
        loans, finep = await asyncio.gather(loans_task, finep_task)
        all_financiamentos = loans + finep

        # 2. Determine eligibility for Tax Incentives
        if clean_cnpj == DEMO_CNPJ:
            direitos = {
                "Lei do Bem (P&D)": {
                    "incentivo": "Lei do Bem (P&D)",
                    "elegivel": True,
                    "motivo_elegibilidade": "Empresa desenvolve P&D/Software e está no Lucro Real",
                    "impacto_estimado": 780000.0,
                    "acao_recomendada": "Ampliar escopo de P&D qualificado na ECF — Bloco M."
                },
                "SUDENE / SUDAM (-75% IRPJ)": {
                    "incentivo": "SUDENE / SUDAM (-75% IRPJ)",
                    "elegivel": True,
                    "orgao": "SUDENE",
                    "motivo_elegibilidade": "Localizada na área de atuação da SUDENE com CNAE elegível e no Lucro Real.",
                    "impacto_estimado": 312000.0,
                    "acao_recomendada": "Protocolar habilitação na SUDENE para redução de 75% no IRPJ no prazo legal."
                },
                "PAT (Alimentação do Trabalhador)": {
                    "incentivo": "PAT (Alimentação do Trabalhador)",
                    "elegivel": True,
                    "motivo_elegibilidade": "Empresas sob Lucro Real podem deduzir custos com alimentação do trabalhador.",
                    "impacto_estimado": 48000.0,
                    "acao_recomendada": "Registrar a empresa no PAT (MTE) e realizar a dedução de até 4% do IRPJ."
                },
                "Desoneração da Folha (CPRB)": {
                    "incentivo": "Desoneração da Folha (CPRB)",
                    "elegivel": True,
                    "motivo_elegibilidade": "CNAE elegível para opção pelo imposto substitutivo sobre receita bruta.",
                    "impacto_estimado": 0.0,
                    "acao_recomendada": "Realizar estudo comparativo entre CPRB (faturamento) e INSS Patronal (20% folha)."
                }
            }
        else:
            lei_do_bem_elig = await TaxIncentiveClient.check_lei_do_bem(cnae, regime, capital_social)
            sudene_elig = await TaxIncentiveClient.check_sudene_sudam(cnae, regime, uf)
            pat_elig = await TaxIncentiveClient.check_pat(regime, capital_social)
            desoneracao_elig = await TaxIncentiveClient.check_desoneracao_folha(cnae)
            
            direitos = {
                "Lei do Bem (P&D)": lei_do_bem_elig,
                "SUDENE / SUDAM (-75% IRPJ)": sudene_elig,
                "PAT (Alimentação do Trabalhador)": pat_elig,
                "Desoneração da Folha (CPRB)": desoneracao_elig,
            }

        # 3. Determine Usage (Uso Efetivo)
        # Default usage profile (simulated based on CNAE/CNPJ or general statistics)
        # If it's the demo CNPJ, we mock a realistic baseline
        if clean_cnpj == DEMO_CNPJ:
            uso_efetivo = {
                "Lei do Bem (P&D)": {"usando": True, "percentual_uso": 40},
                "SUDENE / SUDAM (-75% IRPJ)": {"usando": False, "percentual_uso": 0},
                "PAT (Alimentação do Trabalhador)": {"usando": False, "percentual_uso": 0},
                "Desoneração da Folha (CPRB)": {"usando": True, "percentual_uso": 100},
            }
        else:
            # For other companies, we assume a pessimistic baseline (not using) unless SPED changes it
            uso_efetivo = {
                "Lei do Bem (P&D)": {"usando": False, "percentual_uso": 0},
                "SUDENE / SUDAM (-75% IRPJ)": {"usando": False, "percentual_uso": 0},
                "PAT (Alimentação do Trabalhador)": {"usando": False, "percentual_uso": 0},
                "Desoneração da Folha (CPRB)": {"usando": False, "percentual_uso": 0},
            }

        # Override usage if SPED data is uploaded
        if sped_data:
            if sped_data.get("lei_do_bem_declarado"):
                uso_efetivo["Lei do Bem (P&D)"] = {"usando": True, "percentual_uso": 100}
            if sped_data.get("sudene_declarado"):
                uso_efetivo["SUDENE / SUDAM (-75% IRPJ)"] = {"usando": True, "percentual_uso": 100}
            if sped_data.get("pat_declarado"):
                uso_efetivo["PAT (Alimentação do Trabalhador)"] = {"usando": True, "percentual_uso": 100}
            
            # If the ECF lists any passives, we can merge them into active loans
            if sped_data.get("passivos_bancarios"):
                for pb in sped_data.get("passivos_bancarios"):
                    all_financiamentos.append({
                        "fonte": "SPED (Passivo)",
                        "produto": pb.get("descricao", "Financiamento"),
                        "valor": pb.get("valor", 0.0),
                        "tipo": "Passivo Declarado na ECD",
                        "status": "Declarado"
                    })

        # 4. Perform Gap Analysis
        gap_analysis = GapAnalyzer.analyze(direitos, uso_efetivo)

        # 5. Compute Governance Score
        # Start from 100, deduct for gaps in incentives the company has right to but is not using
        score = 100
        total_gap_value = 0.0
        used_count = 0
        eligible_count = 0

        for gap in gap_analysis:
            if gap["tem_direito"]:
                eligible_count += 1
                if gap["usa"] == "OK":
                    used_count += 1
                elif gap["usa"] == "Aproveitado Parcial":
                    used_count += 1
                    score -= 15
                    total_gap_value += gap["impacto_nao_aproveitado"]
                else:  # Não Aproveitado
                    score -= 30
                    if gap["urgencia"] == "CRÍTICO":
                        score -= 10  # Additional penalty for critical gaps like SUDENE
                    total_gap_value += gap["impacto_nao_aproveitado"]

        score = max(0, min(100, score))
        
        # Build Summary
        if eligible_count > 0:
            resumo = f"Empresa aproveita {used_count} de {eligible_count} incentivos fiscais identificados como elegíveis. Gap estimado de R$ {total_gap_value:,.2f}/ano em benefícios não utilizados."
        else:
            resumo = "Nenhum incentivo tributário federal ou regional relevante identificado para o perfil cadastral atual."

        return {
            "financiamentos": all_financiamentos,
            "gap_analysis": gap_analysis,
            "score_governanca": score,
            "resumo": resumo
        }
