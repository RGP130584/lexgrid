from fastapi import APIRouter
from api.routes import health, sped, mcp_routes
from api.routes import osint

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sped.router, prefix="/sped", tags=["Motor Brasil - SPED"])
api_router.include_router(mcp_routes.router, prefix="/mcp", tags=["Protocolo MCP"])
api_router.include_router(osint.router, prefix="/osint", tags=["OSINT & Inteligência"])