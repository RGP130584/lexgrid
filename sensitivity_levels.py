from enum import IntEnum

class SensitivityLevel(IntEnum):
    """Classificação Corporativa de Sensibilidade da Informação."""
    PUBLIC = 1        # Informação em domínio público (Leis, Diário Oficial)
    INTERNAL = 2      # Uso interno, sem dano se vazado (Políticas gerais)
    CONFIDENTIAL = 3  # Risco moderado, dados de clientes sem PII crítica
    RESTRICTED = 4    # Risco alto, contratos, estratégias corporativas
    SECRET = 5        # Risco crítico, PII, chaves criptográficas, dados financeiros
    
    @classmethod
    def default(cls):
        return cls.CONFIDENTIAL