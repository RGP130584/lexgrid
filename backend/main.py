from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.main_router import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Espinha dorsal cognitiva construída com Clean Architecture"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializacao do banco de dados no startup
@app.on_event("startup")
async def startup_event():
    from infrastructure.database.setup import init_database
    init_database()

# Inclui todas as rotas do sistema centralizadas no main_router
app.include_router(api_router)
