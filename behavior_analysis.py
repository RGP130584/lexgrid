from typing import Dict, Any

class BehaviorAnalyzer:
    """Motor analítico de ameaças para detectar movimentação lateral ou abuso de privilégio."""
    
    @classmethod
    def calculate_risk(cls, subject: Dict[str, Any], action: str, resource: str) -> int:
        """Retorna uma pontuação de 0 a 100 de anomalia."""
        score = 0
        
        # 1. Movimentação Anômala
        if subject.get("location") == "external_ip" and "internal_database" in resource:
            score += 60  # Padrão altamente suspeito
            
        # 2. Exfiltração via IA
        if subject.get("is_ai") and action in ["export", "dump", "query_all"]:
            score += 90  # IA não pode fazer dumps massivos
            
        # 3. Escalada de Privilégio Rápida
        if action == "assume_role" and subject.get("role") != "admin":
            score += 50
            
        return min(score, 100)