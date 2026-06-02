from fastapi import APIRouter
from api.routes import health
from api.routes import sped
from api.routes import mcp_routes
from api.routes import osint

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sped.router, prefix="/sped", tags=["Motor Brasil - SPED"])
api_router.include_router(mcp_routes.router, prefix="/mcp", tags=["Protocolo MCP (Ferramentas de IA)"])
api_router.include_router(osint.router, prefix="/osint", tags=["Deep OSINT"])
