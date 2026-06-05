import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# States eligible for SUDENE (Northeast + parts of MG and ES)
SUDENE_STATES = {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE", "MG", "ES"}
# States eligible for SUDAM (North + parts of MA and MT)
SUDAM_STATES = {"AC", "AP", "AM", "PA", "RO", "RR", "TO", "MA", "MT"}

class TaxIncentiveClient:
    """
    Client and Rule Engine to determine tax incentive eligibility (Federal, Regional, State).
    Checks eligibility rules dynamically based on CNAE, Regime Tributário, and UF (Location).
    """

    @classmethod
    async def check_lei_do_bem(cls, cnae: str, regime: str, capital_social: float) -> Dict[str, Any]:
        """
        Lei do Bem (P&D - Federal) - Eligible for Lucro Real companies performing R&D.
        """
        is_rd_tech = any(cnae.startswith(prefix) for prefix in ["62", "63", "72", "20", "26", "28"])
        is_lucro_real = regime.upper() == "LUCRO REAL"
        
        # Impact estimation: 60% to 80% extra deduction of R&D expenses from IRPJ/CSLL base.
        # Assuming an average R&D expenditure of 5% of estimated revenue or capital social.
        estimated_benefit = 0.0
        if is_rd_tech:
            # High-level estimation of benefit
            estimated_expenditure = max(capital_social * 0.1, 150000.0)
            estimated_benefit = estimated_expenditure * 0.34 * 0.60 # 60% of expenditure times 34% tax rate
            
        return {
            "incentivo": "Lei do Bem (P&D)",
            "elegivel": is_rd_tech and is_lucro_real,
            "motivo_elegibilidade": "Empresa desenvolve P&D/Software e está no Lucro Real" if (is_rd_tech and is_lucro_real)
                                    else ("Apenas para empresas no Lucro Real com CNAE de P&D/Tecnologia/Indústria" if is_rd_tech 
                                    else "CNAE principal não qualifica como P&D/Inovação"),
            "impacto_estimado": estimated_benefit if is_rd_tech else 0.0,
            "acao_recomendada": "Ampliar escopo de P&D qualificado na ECF — Bloco M." if is_lucro_real 
                               else "Migrar para Lucro Real para poder usufruir dos incentivos de P&D."
        }

    @classmethod
    async def check_sudene_sudam(cls, cnae: str, regime: str, uf: str) -> Dict[str, Any]:
        """
        SUDENE / SUDAM (Regional - 75% reduction on IRPJ).
        Eligible for companies in North/Northeast with industrial/infrastructure/eligible services CNAEs, under Lucro Real.
        """
        uf_upper = uf.upper()
        in_sudene = uf_upper in SUDENE_STATES
        in_sudam = uf_upper in SUDAM_STATES
        
        # Eligible CNAEs: Industry (10-33), Infrastructure (35-39), Telecomm (61)
        is_eligible_cnae = any(cnae.startswith(str(prefix)) for prefix in range(10, 40)) or cnae.startswith("61")
        is_lucro_real = regime.upper() == "LUCRO REAL"
        
        eligible = (in_sudene or in_sudam) and is_eligible_cnae and is_lucro_real
        orgao = "SUDENE" if in_sudene else ("SUDAM" if in_sudam else "Regional")
        
        # 75% reduction on IRPJ (15% normal rate + 10% surtax = 25% IRPJ rate).
        # Benefit = 75% of 25% IRPJ = 18.75% of taxable income.
        estimated_benefit = 0.0
        if is_eligible_cnae and (in_sudene or in_sudam):
            estimated_benefit = 312000.0 # Standard demo/industry baseline
            
        return {
            "incentivo": f"{orgao} (-75% IRPJ)",
            "elegivel": eligible,
            "orgao": orgao,
            "motivo_elegibilidade": f"Localizada na área de atuação da {orgao} com CNAE elegível e no Lucro Real." if eligible
                                    else (f"Elegível na região, mas requer regime de Lucro Real" if (in_sudene or in_sudam) and is_eligible_cnae
                                    else "Fora da área geográfica de incentivos regionais (SUDENE/SUDAM)"),
            "impacto_estimado": estimated_benefit if is_eligible_cnae and (in_sudene or in_sudam) else 0.0,
            "acao_recomendada": f"Protocolar habilitação na {orgao} para redução de 75% no IRPJ no prazo legal."
        }

    @classmethod
    async def check_pat(cls, regime: str, capital_social: float) -> Dict[str, Any]:
        """
        PAT - Programa de Alimentação do Trabalhador (Federal).
        Deduction of up to 4% of IRPJ due for Lucro Real companies.
        """
        is_lucro_real = regime.upper() == "LUCRO REAL"
        benefit = 0.0
        if is_lucro_real:
            benefit = max(capital_social * 0.005, 12000.0) # Estimated benefit scale
            
        return {
            "incentivo": "PAT (Alimentação do Trabalhador)",
            "elegivel": is_lucro_real,
            "motivo_elegibilidade": "Empresas sob Lucro Real podem deduzir custos com alimentação do trabalhador." if is_lucro_real else "Requer Lucro Real.",
            "impacto_estimado": benefit if is_lucro_real else 0.0,
            "acao_recomendada": "Registrar a empresa no PAT (MTE) e realizar a dedução de até 4% do IRPJ."
        }

    @classmethod
    async def check_desoneracao_folha(cls, cnae: str) -> Dict[str, Any]:
        """
        Desoneração da Folha (CPRB) - Eligible for specific CNAEs.
        Ex: TI (62), Transport, Construction, Manufacturing.
        """
        is_eligible = any(cnae.startswith(prefix) for prefix in ["62", "63", "41", "42", "43", "13", "14", "15", "16"])
        
        return {
            "incentivo": "Desoneração da Folha (CPRB)",
            "elegivel": is_eligible,
            "motivo_elegibilidade": "CNAE elegível para opção pelo imposto substitutivo sobre receita bruta." if is_eligible else "Setor/CNAE não elegível.",
            "impacto_estimado": 0.0, # Will be calculated by Fator R or active comparison
            "acao_recomendada": "Realizar estudo comparativo entre CPRB (faturamento) e INSS Patronal (20% folha)."
        }
