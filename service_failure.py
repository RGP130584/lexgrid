import subprocess
import time
from observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("Chaos_ServiceFailure")

class ChaosServiceFailure:
    """Implementa Chaos Engineering matando serviços críticos aleatoriamente."""
    
    TARGETS = ["lexgrid_postgres", "lexgrid_qdrant", "lexgrid_dragonfly"]
    
    @classmethod
    def execute_chaos(cls, target: str):
        logger.warning(f"CHAOS MONKEY: Executando Kill/Crash no container {target}")
        subprocess.run(["docker", "kill", target], capture_output=True)
        
    @classmethod
    def validate_recovery(cls, target: str, max_wait_seconds: int = 60) -> bool:
        """Espera e valida se o Agente Zelador (Layer 2) recriou e estabilizou o container."""
        logger.info(f"Monitorando RTO (Recovery Time Objective) do {target}...")
        
        start_time = time.time()
        while (time.time() - start_time) < max_wait_seconds:
            res = subprocess.run(
                ["docker", "inspect", "--format={{.State.Status}}", target], 
                capture_output=True, text=True
            )
            status = res.stdout.strip()
            if status == "running":
                rto = round(time.time() - start_time, 2)
                logger.info(f"[{target}] RECUPERADO. RTO: {rto} segundos.")
                return True
                
            time.sleep(2)
            
        logger.critical(f"[{target}] FALHA NA RECUPERAÇÃO. Auto-healing não respondeu a tempo.")
        return False