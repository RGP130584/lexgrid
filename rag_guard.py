from enum import Enum

class SensitivityLevel(Enum):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED = 4
    SECRET = 5

class RAGGuard:
    """Controla o nível de acesso do RAG para evitar Data Leakage inter-departamental."""
    
    @classmethod
    def validate_retrieval(cls, user_clearance: SensitivityLevel, doc_classification: SensitivityLevel) -> bool:
        """Garante Least Privilege no contexto injetado no LLM."""
        return user_clearance.value >= doc_classification.value

    @classmethod
    def filter_context(cls, documents: list[dict], user_clearance: SensitivityLevel) -> list[dict]:
        """Filtra fragmentos vetoriais antes de enviar ao modelo."""
        return [
            doc for doc in documents 
            if doc.get("metadata", {}).get("classification", 1) <= user_clearance.value
        ]