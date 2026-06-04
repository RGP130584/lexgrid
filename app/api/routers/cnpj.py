from fastapi import APIRouter, HTTPException, Request
from app.api.schemas.cnpj_response import CNPJResponse
from app.services.enrichment.cnpj_enrichment_service import CNPJEnrichmentService
from app.core.security.rate_limit import check_rate_limit

router = APIRouter()

@router.get("/{cnpj}", response_model=CNPJResponse)
async def analyze_cnpj(request: Request, cnpj: str):
    check_rate_limit(request, limit=20, window=60)
    
    try:
        response = await CNPJEnrichmentService.analyze(cnpj)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno no Enrichment Engine.")