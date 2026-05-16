from fastapi import APIRouter, UploadFile, File, HTTPException
from application.use_cases.sped_ingestion import SpedIngestionUseCase
from infrastructure.database.postgres_sped_repository import PostgresSpedRepository

router = APIRouter()


@router.post("/ingest", response_model=dict)
async def ingest_sped_file(file: UploadFile = File(...)):
    """Recebe e processa arquivos magnéticos governamentais (SPED)"""
    
    if not file.filename.upper().endswith((".TXT", ".SPED")):
        raise HTTPException(status_code=400, detail="Formato inválido. Envie um arquivo .txt do SPED.")
    
    # O SPED tradicionalmente utiliza codificação ISO-8859-1 / Latin-1
    content_bytes = await file.read()
    content_text = content_bytes.decode("iso-8859-1")
    
    # Instancia o repositório e injeta no Caso de Uso (Injeção de Dependência Manual)
    repo = PostgresSpedRepository()
    use_case = SpedIngestionUseCase(repository=repo)
    sped_data = use_case.execute(filename=file.filename, content=content_text)
    
    return {
        "status": "sucesso",
        "arquivo": sped_data.filename,
        "tipo_identificado": sped_data.file_type,
        "total_registros_lidos": len(sped_data.records)
    }