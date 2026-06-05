import httpx
from app.core.logging.logger import get_logger
from app.core.config.settings import settings

logger = get_logger("ReceitaClient")

class ReceitaClient:
    @staticmethod
    async def fetch_cnpj_data(cnpj: str) -> dict:
        url = f"{settings.RECEITA_API_URL}/{cnpj}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logger.error(f"Erro BrasilAPI: {e}")
                
        # Fallback ReceitaWS
        url_ws = f"{settings.RECEITA_WS_URL}/{cnpj}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url_ws)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "ERROR":
                        return {}
                    return ReceitaClient._normalize_receitaws(data)
            except Exception as e:
                logger.error(f"Erro ReceitaWS: {e}")
                
        return {}

    @staticmethod
    async def fetch_pgfn_debts(cnpj: str) -> list:
        # BrasilAPI endpoint de dívida ativa da união
        url = f"https://brasilapi.com.br/api/pgfn/v1/{cnpj}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logger.error(f"Erro ao buscar dívidas PGFN: {e}")
        return []

    @staticmethod
    def _normalize_receitaws(data: dict) -> dict:
        return {
            "cnpj": data.get("cnpj", "").replace(".", "").replace("-", "").replace("/", ""),
            "razao_social": data.get("nome"),
            "nome_fantasia": data.get("fantasia"),
            "natureza_juridica": data.get("natureza_juridica"),
            "capital_social": float(data.get("capital_social", 0.0)),
            "uf": data.get("uf"),
            "municipio": data.get("municipio"),
            "porte": data.get("porte"),
            "descricao_situacao_cadastral": data.get("situacao"),
            "cnae_fiscal": data.get("atividade_principal", [{}])[0].get("code", "").replace(".", "").replace("-", ""),
            "cnae_fiscal_descricao": data.get("atividade_principal", [{}])[0].get("text"),
            "cnaes_secundarios": [{"codigo": c.get("code", "").replace(".", "").replace("-", ""), "descricao": c.get("text")} for c in data.get("atividades_secundarias", [])],
            "qsa": [{"nome_socio": s.get("nome"), "qualificacao_socio": s.get("qual")} for s in data.get("qsa", [])]
        }