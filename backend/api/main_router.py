from fastapi import APIRouter
from api.routes import health
from api.routes import sped_routes
from api.routes import mcp_routes
from api.routes import osint
from app.api.routers import cnpj
from app.api.routers import opportunities

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sped_routes.router, prefix="/sped", tags=["Motor Brasil - SPED"])
api_router.include_router(mcp_routes.router, prefix="/mcp", tags=["Protocolo MCP (Ferramentas de IA)"])
api_router.include_router(osint.router, prefix="/osint", tags=["Deep OSINT"])
api_router.include_router(cnpj.router, prefix="/api/v1/cnpj", tags=["CNPJ Intelligence"])
api_router.include_router(opportunities.router, prefix="/api/v1/opportunities", tags=["Opportunity Intelligence"])
