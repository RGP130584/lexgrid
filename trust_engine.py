from typing import Dict, Any
from ..iam.abac import ABACEngine
from ..threat_detection.behavior_analysis import BehaviorAnalyzer

class ZeroTrustEngine:
    """
    Motor de Avaliação Contínua de Confiança.
    Nenhum usuário, sistema ou IA recebe acesso implícito.
    """
    
    @classmethod
    def evaluate_access(cls, subject: Dict[str, Any], resource: str, action: str, context: Dict[str, Any]) -> bool:
        """
        Avalia se a solicitação de acesso deve ser permitida com base em 
        Atributos (ABAC) e Comportamento Analítico.
        """
        
        # 1. Validação de Atributos e Políticas (ABAC / Least Privilege)
        if not ABACEngine.is_allowed(subject, resource, action, context):
            return False
            
        # 2. Verificação de Saúde da Sessão / Dispositivo
        if not cls._validate_session_trust(subject, context):
            return False
            
        # 3. Análise de Risco Comportamental Contínua
        risk_score = BehaviorAnalyzer.calculate_risk(subject, action, resource)
        if risk_score > 80:  # Threshold crítico de anomalia
            return False
            
        return True

    @classmethod
    def _validate_session_trust(cls, subject: Dict[str, Any], context: Dict[str, Any]) -> bool:
        # Mock de validação de token revogado, IP de origem, e mTLS
        if context.get("ip_reputation") == "malicious":
            return False
        return True