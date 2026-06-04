from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import cnpj
from app.api.routers import opportunities
from app.core.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CNPJ Enrichment Engine - LexGrid MVP"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/", tags=["Status"])
async def root():
    """Rota raiz (Health Check) da API LexGrid."""
    return {
        "status": "online", 
        "projeto": settings.PROJECT_NAME, 
        "mensagem": "Motor de Enriquecimento CNPJ operante. Acesse /docs para a documentação."
    }

app.include_router(cnpj.router, prefix="/api/v1/cnpj", tags=["CNPJ Intelligence"])
app.include_router(opportunities.router, prefix="/api/v1/opportunities", tags=["Opportunity Intelligence"])