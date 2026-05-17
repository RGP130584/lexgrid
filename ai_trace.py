import hashlib
from ..logging.structured_logger import get_structured_logger

logger = get_structured_logger("ai_trace")

class AITracer:
    """Rastreia interações com LLMs para auditoria fiduciária e billing."""
    
    @staticmethod
    def log_inference(model: str, prompt: str, response: str, tokens: int, latency_ms: float, docs_retrieved: int):
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        
        extra_context = {
            "ai_model": model,
            "prompt_hash": prompt_hash,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "tokens_used": tokens,
            "latency_ms": latency_ms,
            "docs_retrieved": docs_retrieved,
            "cost_estimate_usd": (tokens / 1000) * 0.002 # Placeholder
        }
        
        # Usamos extra_info para acoplar dados estruturados via dict
        logger.info(
            f"AI Inference via {model} completada em {latency_ms}ms",
            extra={"extra_info": extra_context}
        )