from .port_manager import PortManager
from .healthcheck import HealthCheck

class Readiness:
    def __init__(self, healthcheck: HealthCheck, logger):
        self.healthcheck = healthcheck
        self.logger = logger

    def is_ready(self, services: dict) -> bool:
        self.logger.info("Validando Readiness (Health + Ports)...")
        ready = True
        for name, config in services.items():
            if not self.healthcheck.check_service(config["container"]):
                self.logger.warning(f"Serviço {name} não está healthy.")
                ready = False
            elif not PortManager.is_port_open(config["port"]):
                self.logger.warning(f"Porta {config['port']} do serviço {name} não está respondendo.")
                ready = False
            else:
                self.logger.info(f"[OK] {name} pronto e respondendo.")
        return ready