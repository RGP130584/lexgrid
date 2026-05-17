from enum import Enum

class AIRiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class AIRiskMatrix:
    """Avaliação de Risco para Ativos de IA."""
    
    @classmethod
    def evaluate_use_case(cls, contains_pii: bool, affects_financials: bool, is_autonomous: bool) -> AIRiskLevel:
        if affects_financials and is_autonomous:
            return AIRiskLevel.CRITICAL
        if contains_pii or affects_financials:
            return AIRiskLevel.HIGH
        return AIRiskLevel.MEDIUM if is_autonomous else AIRiskLevel.LOW