from .docker_manager import DockerManager
from .network_manager import NetworkManager
from .volume_manager import VolumeManager
from .healthcheck import HealthCheck
from .readiness import Readiness
from .recovery_engine import RecoveryEngine
from .diagnostics import Diagnostics
from .retry_engine import RetryEngine
from .service_registry import ServiceRegistry
from .constants import VOLUMES

class Orchestrator:
    def __init__(self, obs):
        self.logger = obs.get_logger()
        self.docker = DockerManager(self.logger)
        self.network = NetworkManager(self.logger)
        self.volume = VolumeManager(self.logger)
        self.health = HealthCheck(self.docker)
        self.readiness = Readiness(self.health, self.logger)
        self.recovery = RecoveryEngine(self.docker, self.network, self.volume, self.logger)
        self.diagnostics = Diagnostics(self.health)
        self.services = ServiceRegistry.get_services()

    def check_status(self) -> bool:
        if not self.docker.is_engine_running():
            self.logger.error("Docker Engine offline.")
            return False
        return self.readiness.is_ready(self.services)

    def heal(self):
        self.logger.info("Iniciando fluxo de Auto-Healing...")
        if self.check_status():
            self.logger.info("Infraestrutura está saudável. Nenhum reparo necessário.")
            return True
            
        self.recovery.execute_tactic_1_soft_restart()
        if RetryEngine.execute_with_backoff(self.check_status, self.logger):
            return True
            
        self.recovery.execute_tactic_2_hard_restart()
        if RetryEngine.execute_with_backoff(self.check_status, self.logger):
            return True
            
        self.logger.error("Falha no healing padrão. Tática Nuclear manual exigida.")
        return False

    def nuclear_recovery(self):
        self.recovery.execute_tactic_3_nuclear(VOLUMES)
        return RetryEngine.execute_with_backoff(self.check_status, self.logger)

    def generate_diagnostics(self) -> dict:
        return self.diagnostics.run_full_diagnosis()