from typing import List, Dict, Any

class RiskScoringEngine:
    @classmethod
    def calculate_scores(
        cls,
        cnpj: str,
        divida_ativa: List[Dict[str, Any]],
        capital_social: float,
        background_check: Dict[str, Any],
        lawsuits: List[Dict[str, Any]],
        cyber_risks: Dict[str, Any],
        market_risks: Dict[str, Any],
        faturamento_estimado: float,
        protestos: List[Dict[str, Any]] = []
    ) -> Dict[str, float]:
        """
        Calcula as pontuações de risco baseadas no ARD.
        Retorna as pontuações normalizadas (0 a 100, onde 100 é o melhor cenário).
        """
        # 1. Risco Financeiro (Peso: 40%)
        score_financeiro = 100.0
        # Subtrai por dívida ativa PGFN
        if divida_ativa:
            score_financeiro -= (len(divida_ativa) * 25.0)
        # Subtrai por títulos protestados em cartório (Alta Severidade)
        if protestos:
            score_financeiro -= (len(protestos) * 20.0)
        # Subtrai por indicativo de sub-capitalização (capital social baixo vs faturamento presumido alto)
        if capital_social > 0 and faturamento_estimado > (capital_social * 5.0) and capital_social < 100000.0:
            score_financeiro -= 15.0
            
        score_financeiro = max(0.0, min(100.0, score_financeiro))

        # 2. Risco Compliance / Tributário (Peso: 30%)
        score_compliance = 100.0
        # Subtrai por processos judiciais ativos
        if lawsuits:
            for processo in lawsuits:
                classe = processo.get("classe", "").lower()
                status = processo.get("status", "").lower()
                if "execução fiscal" in classe or "tributária" in classe:
                    score_compliance -= 20.0
                elif "trabalhista" in classe:
                    score_compliance -= 15.0
                else:
                    score_compliance -= 10.0
        
        # Subtrai por antecedentes criminais de sócios ou mandados de prisão
        antecedentes = background_check.get("antecedentes_criminais", [])
        for ant in antecedentes:
            if ant.get("status") != "NADA CONSTA":
                score_compliance -= 25.0
                
        mandados = background_check.get("mandados_prisao", [])
        if mandados:
            score_compliance -= (len(mandados) * 30.0)

        score_compliance = max(0.0, min(100.0, score_compliance))

        # 3. Risco Operacional / Cibernético (Peso: 15%)
        score_cibernetico = 100.0
        vulns = cyber_risks.get("vulnerabilidades_ciberneticas", [])
        for v in vulns:
            crit = v.get("criticidade", "").upper()
            if crit == "CRÍTICA":
                score_cibernetico -= 30.0
            elif crit == "ALTA":
                score_cibernetico -= 20.0
            else:
                score_cibernetico -= 10.0
                
        leaks = cyber_risks.get("leaks_detectados", [])
        if leaks:
            score_cibernetico -= (len(leaks) * 15.0)

        score_cibernetico = max(0.0, min(100.0, score_cibernetico))

        # 4. Risco de Mercado / Liquidez (Peso: 15%)
        score_mercado = 100.0
        selic = market_risks.get("taxa_selic", 10.5)
        pressao = market_risks.get("pressao_setorial", "").upper()
        
        if selic > 10.0:
            if "ALTA" in pressao:
                score_mercado -= 20.0
            elif "MÉDIA" in pressao:
                score_mercado -= 10.0
            else:
                score_mercado -= 5.0
                
        if "ALTA" in pressao:
            score_mercado -= 15.0
        elif "MÉDIA" in pressao:
            score_mercado -= 10.0

        score_mercado = max(0.0, min(100.0, score_mercado))

        # 5. Score Global (Média Ponderada)
        score_global = (
            (score_financeiro * 0.40) +
            (score_compliance * 0.30) +
            (score_cibernetico * 0.15) +
            (score_mercado * 0.15)
        )
        
        # Limita e arredonda
        score_global = round(max(0.0, min(100.0, score_global)), 1)
        score_financeiro = round(score_financeiro, 1)
        score_compliance = round(score_compliance, 1)
        score_cibernetico = round(score_cibernetico, 1)
        score_mercado = round(score_mercado, 1)

        return {
            "score_global": score_global,
            "score_financeiro": score_financeiro,
            "score_compliance": score_compliance,
            "score_cibernetico": score_cibernetico,
            "score_mercado": score_mercado
        }
