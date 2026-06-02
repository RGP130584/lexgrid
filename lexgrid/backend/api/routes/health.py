from fastapi import APIRouter
from application.use_cases.health_check import HealthCheckUseCase

router = APIRouter()


@router.get("/health", response_model=dict)
def check_health():
    use_case = HealthCheckUseCase()
    status = use_case.execute()
    return {
        "status": status.status,
        "system": status.system,
        "version": status.version
    }