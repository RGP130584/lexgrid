import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GapAnalyzer:
    """
    Analyzes the gaps between the tax incentives a company has the right to use (Elegibilidade)
    and what it actually uses (Uso Efetivo, e.g. via SPED or declarations).
    """

    @staticmethod
    def analyze(direito_dict: Dict[str, Dict[str, Any]], uso_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Compares eligibility (direito) and active usage (uso) to identify optimization gaps.
        
        :param direito_dict: Dict of incentive name -> eligibility payload from TaxIncentiveClient.
        :param uso_dict: Dict of incentive name -> usage details (e.g. {'usando': True/False, 'valor': float})
        :return: List of gap analysis results.
        """
        gaps = []
        
        for name, info in direito_dict.items():
            elig = info.get("elegivel", False)
            usage = uso_dict.get(name, {})
            usando = usage.get("usando", False)
            percentual = usage.get("percentual_uso", 100) if usando else 0
            
            status = "N/A"
            urgencia = "N/A"
            impacto = 0.0
            acao = info.get("acao_recomendada", "Nenhuma ação necessária.")
            
            if elig:
                if usando:
                    if percentual < 100:
                        status = "Aproveitado Parcial"
                        urgencia = "MÉDIO" if name != "Lei do Bem (P&D)" else "ALTO"
                        # Gap is the remaining percentage of the estimated benefit
                        impacto = info.get("impacto_estimado", 0.0) * (1 - percentual / 100)
                        if name == "Lei do Bem (P&D)":
                            acao = "Ampliar mapeamento de horas e projetos elegíveis de P&D no Bloco M da ECF."
                    else:
                        status = "OK"
                        urgencia = "OK"
                        impacto = 0.0
                        acao = "Benefício aproveitado corretamente."
                else:
                    status = "Não Aproveitado"
                    urgencia = "ALTO"
                    if "SUDENE" in name or "SUDAM" in name:
                        urgencia = "CRÍTICO"
                    impacto = info.get("impacto_estimado", 0.0)
                    acao = info.get("acao_recomendada", "")
            else:
                status = "Não Elegível"
                urgencia = "N/A"
                impacto = 0.0
                if "SUDENE" in name or "SUDAM" in name:
                    acao = "Empresa fora da área regional elegível ou não enquadrada no Lucro Real."
                elif "Lei do Bem" in name:
                    acao = "Requer regime tributário de Lucro Real e atividade de inovação."
                else:
                    acao = "Perfil cadastral ou setorial não qualifica para este benefício."
                    
            gaps.append({
                "incentivo": name,
                "tem_direito": elig,
                "usa": status if elig else False,
                "uso_percentual": percentual if usando else 0,
                "impacto_nao_aproveitado": impacto,
                "urgencia": urgencia,
                "acao": acao
            })
            
        return gaps
