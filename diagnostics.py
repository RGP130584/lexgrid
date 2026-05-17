from .port_manager import PortManager
from .service_registry import ServiceRegistry
from .healthcheck import HealthCheck

class Diagnostics:
    def __init__(self, healthcheck: HealthCheck):
        self.healthcheck = healthcheck

    def run_full_diagnosis(self) -> dict:
        services = ServiceRegistry.get_services()
        health_status = self.healthcheck.get_all_status(services)
        ports_to_check = [s["port"] for s in services.values()]
        port_conflicts = PortManager.check_conflicts(ports_to_check)
        
        return {
            "services": services,
            "container_health": health_status,
            "port_bindings": port_conflicts
        }