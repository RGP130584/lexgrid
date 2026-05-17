from .docker_manager import DockerManager
from .network_manager import NetworkManager
from .volume_manager import VolumeManager
from .circuit_breaker import CircuitBreaker

class RecoveryEngine:
    def __init__(self, docker: DockerManager, network: NetworkManager, volume: VolumeManager, logger):
        self.docker = docker
        self.network = network
        self.volume = volume
        self.logger = logger
        self.breaker = CircuitBreaker()

    def execute_tactic_1_soft_restart(self):
        if self.breaker.is_open("global_recovery"):
            self.logger.error("Circuit Breaker ABERTO. Impedindo loop infinito de recovery.")
            return False
        self.logger.warning("Recovery Tática 1: Soft Restart / Force Recreate")
        self.breaker.record_failure("global_recovery")
        return self.docker.compose_up(force_recreate=True)

    def execute_tactic_2_hard_restart(self):
        self.logger.warning("Recovery Tática 2: Down & Up + Prune Networks")
        self.docker.compose_down()
        self.network.prune_networks()
        return self.docker.compose_up()

    def execute_tactic_3_nuclear(self, volumes_to_wipe: list):
        self.logger.error("Recovery Tática 3: NUCLEAR (Wipe Volumes & Data)")
        self.docker.compose_down(remove_volumes=True)
        self.volume.purge_volumes(volumes_to_wipe)
        self.network.prune_networks()
        res = self.docker.compose_up()
        if res:
            self.breaker.reset("global_recovery")
        return res