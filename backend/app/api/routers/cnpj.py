from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from app.api.schemas.cnpj_response import CNPJResponse
from app.services.enrichment.cnpj_enrichment_service import CNPJEnrichmentService
from app.core.security.rate_limit import check_rate_limit
from app.engines.incentive_engine.sped_parser import SPEDParser

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

@router.post("/upload-sped", response_model=CNPJResponse)
async def upload_sped(
    cnpj: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        content = await file.read()
        text_content = content.decode("utf-8", errors="replace")
        
        filename = file.filename.lower()
        sped_data = {}
        if "ecf" in filename:
            sped_data = SPEDParser.parse_ecf(text_content)
        elif "contrib" in filename or "fd" in filename:
            sped_data = SPEDParser.parse_efd_contribuicoes(text_content)
        elif "icms" in filename or "ipi" in filename:
            sped_data = SPEDParser.parse_efd_icms_ipi(text_content)
        else:
            ecf = SPEDParser.parse_ecf(text_content)
            efd_c = SPEDParser.parse_efd_contribuicoes(text_content)
            efd_i = SPEDParser.parse_efd_icms_ipi(text_content)
            sped_data = {**ecf, **efd_c, **efd_i}
            
        response = await CNPJEnrichmentService.analyze(cnpj, sped_data=sped_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo SPED: {str(e)}")