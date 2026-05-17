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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cnpj.router, prefix="/api/v1/cnpj", tags=["CNPJ Intelligence"])
app.include_router(opportunities.router, prefix="/api/v1/opportunities", tags=["Opportunity Intelligence"])