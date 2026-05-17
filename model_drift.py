from collections import deque
import numpy as np

class ModelBehaviorDrift:
    """Detecta desvio de comportamento contínuo nas respostas do LLM ao longo do tempo."""
    
    def __init__(self, window_size: int = 100):
        self.confidence_window = deque(maxlen=window_size)
        self.latency_window = deque(maxlen=window_size)
        self.drift_threshold_std = 2.5 # 2.5 Desvios Padrões

    def register_interaction(self, confidence_score: float, latency_ms: float) -> bool:
        """Registra e retorna True se detectar um Drift anômalo no comportamento (ex: modelo degradado)."""
        if len(self.confidence_window) > 10:
            mean_conf = np.mean(self.confidence_window)
            std_conf = np.std(self.confidence_window)
            
            # Se a confiança da resposta cair abruptamente, temos um Behavior Drift
            if confidence_score < (mean_conf - self.drift_threshold_std * std_conf):
                return True # Drift Detectado!
                
        self.confidence_window.append(confidence_score)
        self.latency_window.append(latency_ms)
        return False