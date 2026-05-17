import time
from .config import RetryConfig

class RetryEngine:
    @staticmethod
    def execute_with_backoff(operation, logger, *args, **kwargs):
        delay = RetryConfig.BASE_DELAY
        
        for attempt in range(1, RetryConfig.MAX_RETRIES + 1):
            try:
                result = operation(*args, **kwargs)
                if result:
                    return result
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt}: {str(e)}")
            
            if attempt < RetryConfig.MAX_RETRIES:
                logger.warning(f"Tentativa {attempt} falhou. Retentando em {delay}s...")
                time.sleep(delay)
                delay = min(delay * 2, RetryConfig.MAX_DELAY)
                
        logger.error(f"Operação falhou permanentemente após {RetryConfig.MAX_RETRIES} tentativas.")
        return False