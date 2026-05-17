import re
from .sensitivity_levels import SensitivityLevel

class DataClassifier:
    """Motor automático de classificação e tagueamento de dados."""

    @classmethod
    def classify_text(cls, content: str) -> SensitivityLevel:
        content_lower = content.lower()
        
        # Heurística: Dados Fiscais/Financeiros/Senhas
        if re.search(r'(senha|password|private key|token|api[_-]?key)', content_lower):
            return SensitivityLevel.SECRET
            
        # Heurística: PII Brasileiro e Cartões
        if re.search(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', content) or re.search(r'\b(?:\d[ -]*?){13,16}\b', content):
            return SensitivityLevel.SECRET
            
        # Heurística: Restrito / Contratos
        if "contrato" in content_lower or "balanço" in content_lower or "sped" in content_lower:
            return SensitivityLevel.RESTRICTED
            
        # Heurística: Público
        if "diário oficial" in content_lower or "lei nº" in content_lower:
            return SensitivityLevel.PUBLIC
            
        # Fallback
        return SensitivityLevel.CONFIDENTIAL