import re

class HallucinationEvaluator:
    """Motor de avaliação contínua para Factuality e Groundedness em RAG."""
    
    @classmethod
    def evaluate_groundedness(cls, context_documents: str, llm_response: str) -> float:
        """
        Heurística simplificada de N-Gram Overlap para medir aderência ao contexto.
        Em produção, pode chamar um modelo "Judge" mais leve (ex: MiniLM).
        """
        if not context_documents.strip():
            return 0.0 # Sem contexto, chance máxima de alucinação (Zero-shot)
            
        # Limpeza básica
        context_words = set(re.findall(r'\w+', context_documents.lower()))
        response_words = set(re.findall(r'\w+', llm_response.lower()))
        
        if not response_words:
            return 0.0
            
        # Calcula o overlap de palavras (Recall em relação ao contexto)
        # Desconsiderando stop-words em uma impl mais robusta
        intersection = response_words.intersection(context_words)
        overlap_score = len(intersection) / len(response_words)
        
        return overlap_score * 100.0 # Retorna de 0 a 100% de aderência fática