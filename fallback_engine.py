import logging
from typing import Callable, Any

logger = logging.getLogger("FallbackEngine")

class AIReliabilityEngine:
    """Garante resiliência transacional através de Circuit Breaking e Fallback de Modelos."""
    
    @classmethod
    def execute_with_fallback(cls, primary_callable: Callable, fallback_callable: Callable, *args, **kwargs) -> Any:
        """
        Tenta executar o modelo principal (ex: Qwen local via Ollama).
        Em caso de timeout, falha ou bloqueio, escala para o modelo fallback (ex: Llama3 menor ou API Externa Segura).
        """
        try:
            logger.info("Tentando inferência via Modelo Primário...")
            response = primary_callable(*args, **kwargs)
            return response
        except Exception as e:
            logger.error(f"Falha no Modelo Primário: {e}. Acionando Fallback/Degradação Controlada.")
            
            try:
                # Tenta o modelo menor/secundário
                response_fallback = fallback_callable(*args, **kwargs)
                return response_fallback
            except Exception as e_fallback:
                logger.critical(f"Falha total na Cadeia de Modelos (Primário e Secundário). {e_fallback}")
                return {"error": "Serviço Cognitivo indisponível no momento. Degradação operacional ativada."}