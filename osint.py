from fastapi import APIRouter, HTTPException
from infrastructure.osint.crawl_service import CrawlService
from pydantic import BaseModel

router = APIRouter()

class OsintRequest(BaseModel):
    url: str

@router.post("/deep-search")
async def deep_search(request: OsintRequest):
    """
    Executa uma varredura OSINT em uma URL governamental ou jurídica.
    """
    crawler = CrawlService()
    markdown_content = await crawler.fetch_government_data(request.url)
    
    if "Erro ao acessar" in markdown_content:
        raise HTTPException(status_code=500, detail=markdown_content)
        
    return {
        "source": request.url,
        "content_summary": markdown_content[:500] + "...", # Retorna os primeiros 500 caracteres
        "full_content_length": len(markdown_content)
    }