from domain.entities.health import SystemStatus
from core.config import settings


class HealthCheckUseCase:
    def execute(self) -> SystemStatus:
        # Em um caso real, este Use Case consultaria repositórios de banco de dados
        # injetados no construtor da classe antes de retornar o status.
        return SystemStatus(
            status="online",
            system=settings.PROJECT_NAME,
            version=settings.VERSION
        )