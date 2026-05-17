import re
from typing import Any

class LogSanitizer:
    """Remove informações sensíveis antes da persistência de logs (LGPD e Security)."""
    
    SENSITIVE_KEYS = {"password", "secret", "token", "api_key", "authorization", "cpf", "credit_card"}
    
    @classmethod
    def sanitize_dict(cls, data: dict) -> dict:
        sanitized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in cls.SENSITIVE_KEYS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_dict(value)
            elif isinstance(value, str):
                sanitized[key] = cls.sanitize_string(value)
            else:
                sanitized[key] = value
        return sanitized

    @classmethod
    def sanitize_string(cls, text: str) -> str:
        # Regex básico para capturar padrões vazados no log (Tokens, Senhas)
        text = re.sub(r"(?i)(bearer|token|key)[\s:=]+[\"']?[A-Za-z0-9\-_]{16,}[\"']?", r"\1 [REDACTED]", text)
        text = re.sub(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "[REDACTED_CPF]", text)
        return text