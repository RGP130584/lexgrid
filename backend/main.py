from fastapi import FastAPI
from api.main_router import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Espinha dorsal cognitiva construída com Clean Architecture"
)

# Inclui todas as rotas do sistema centralizadas no main_router
app.include_router(api_router)
