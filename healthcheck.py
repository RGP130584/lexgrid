from .docker_manager import DockerManager

class HealthCheck:
    def __init__(self, docker_manager: DockerManager):
        self.docker = docker_manager

    def check_service(self, container_name: str) -> bool:
        status = self.docker.get_container_status(container_name)
        return status in ["healthy", "running"]
        
    def get_all_status(self, services: dict) -> dict:
        results = {}
        for name, config in services.items():
            container = config["container"]
            results[name] = self.docker.get_container_status(container)
        return results