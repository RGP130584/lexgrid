import numpy as np
from typing import List

class EmbeddingPoisoningDetector:
    """Detecta ataques de envenenamento vetorial (Data Poisoning) em ingestões de RAG."""
    
    # Thresholds aprendidos a partir de baselines de modelos de embedding
    MAX_L2_NORM = 2.0
    MIN_L2_NORM = 0.5

    @classmethod
    def is_vector_safe(cls, vector: List[float]) -> bool:
        """
        Valida se o embedding possui uma distribuição e norma L2 esperadas.
        Vetores anômalos (com injeções matemáticas) tendem a distorcer a norma.
        """
        arr = np.array(vector)
        if np.isnan(arr).any() or np.isinf(arr).any():
            return False
            
        norm = np.linalg.norm(arr)
        return cls.MIN_L2_NORM <= norm <= cls.MAX_L2_NORM