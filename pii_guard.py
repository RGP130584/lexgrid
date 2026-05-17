import re

class PIIGuard:
    """
    Sanitização de PII e Segredos para LGPD Compliance.
    Nota: Em produção enterprise, integra-se com Microsoft Presidio.
    """
    
    PATTERNS = {
        "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
        "API_KEY": r"(?i)(api[_-]?key|secret|token)[\s:=]+[\"']?[A-Za-z0-9\-_]{16,}[\"']?"
    }

    @classmethod
    def mask_data(cls, text: str) -> str:
        """Mascaramento unidirecional de dados sensíveis no output da IA."""
        sanitized = text
        for entity_type, pattern in cls.PATTERNS.items():
            sanitized = re.sub(pattern, f"[REDACTED_{entity_type}]", sanitized)
        return sanitized

    @classmethod
    def detect_leakage(cls, text: str) -> bool:
        """Verifica se há PII crítico vazando (para auditoria ou bloqueio duro)."""
        for entity_type, pattern in cls.PATTERNS.items():
            # Ignoramos EMAIL para bloqueio duro, mas bloqueamos Cartões e API Keys
            if entity_type in ["CREDIT_CARD", "API_KEY"]:
                if re.search(pattern, text):
                    return True
        return False