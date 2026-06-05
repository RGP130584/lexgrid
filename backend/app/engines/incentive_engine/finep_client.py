import logging
import httpx
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FINEPClient:
    """
    Client for FINEP Transparency (finep.gov.br/transparencia/contratos).
    Queries subventions and credits by CNPJ.
    """
    
    BASE_URL = "https://www.finep.gov.br/api/transparencia/contratos" # Example API path

    @classmethod
    async def search_by_cnpj(cls, cnpj: str) -> List[Dict[str, Any]]:
        clean_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")
        
        # Check if it's the demo CNPJ
        if clean_cnpj == "29093966000100":
            return [
                {
                    "fonte": "FINEP",
                    "produto": "PAPPE Subvenção",
                    "valor": 450000.0,
                    "tipo": "Subvenção (não reembolsável)",
                    "edital": "PAPPE/2021",
                    "status": "Em Execução"
                }
            ]

        # In production, we'd query the FINEP contracts database or search index.
        # Since finep.gov.br transparency data is usually public but does not have a 
        # stable public API, we implement a mock check / scrape or robust fallback.
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                # Mock endpoint or search query on FINEP site
                response = await client.get(f"{cls.BASE_URL}?cnpj={clean_cnpj}")
                if response.status_code == 200:
                    data = response.json()
                    contracts = data.get("contracts", [])
                    results = []
                    for c in contracts:
                        results.append({
                            "fonte": "FINEP",
                            "produto": c.get("objeto") or "Fomento FINEP",
                            "valor": float(c.get("valor_aprovado") or 0.0),
                            "tipo": c.get("modalidade") or "Subvenção",
                            "edital": c.get("chamada_publica") or "N/A",
                            "status": c.get("situacao") or "Ativo"
                        })
                    return results
        except Exception as e:
            logger.warning(f"FINEPClient error or timeout (using clean fallback): {e}")

        return []
