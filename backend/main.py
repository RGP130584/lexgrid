from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.main_router import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Espinha dorsal cognitiva construída com Clean Architecture"
)

# Configuração de CORS para o Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui todas as rotas do sistema centralizadas no main_router
app.include_router(api_router)