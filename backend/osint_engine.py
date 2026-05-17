import httpx
import asyncio
from fastapi import HTTPException
from api.models.diagnostico import DiagnosticoRequest

# Configuração interna
MCP_SERVERS = {
    "n8n_bridge": "http://localhost:5678/webhook/lexgrid-integration" 
}

async def call_mcp_tool_universal_master(cnpj: str) -> dict:
    """Executa a cascata de busca OSINT via protocolo MCP."""
    url_brasil_api = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url_brasil_api)
            if response.status_code == 200:
                dados = response.json()
                # Normalização BrasilAPI para o padrão LexGrid
                return {
                    "fonte": "BrasilAPI",
                    "razao_social": dados.get("razao_social"),
                    "nome_fantasia": dados.get("nome_fantasia") or dados.get("razao_social"),
                    "capital_social": float(dados.get("capital_social", 0.0)),
                    "descricao_situacao_cadastral": dados.get("descricao_situacao_cadastral"),
                    "natureza_juridica": dados.get("natureza_juridica"),
                    "cnae_fiscal": str(dados.get("cnae_fiscal", "")),
                    "cnae_fiscal_descricao": dados.get("cnae_fiscal_descricao"),
                    "cnaes_secundarios": [{"codigo": str(c.get("codigo", "")), "descricao": c.get("descricao")} for c in dados.get("cnaes_secundarios", [])],
                    "qsa": [{"nome_socio": s.get("nome_socio"), "qualificacao_socio": s.get("qualificacao_socio")} for s in dados.get("qsa", [])]
                }
        except Exception:
            pass

    url_receitaws = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url_receitaws)
            if response.status_code == 200:
                dados = response.json()
                return {
                    "fonte": "ReceitaWS",
                    "razao_social": dados.get("nome"),
                    "nome_fantasia": dados.get("fantasia"),
                    "capital_social": float(dados.get("capital_social", 0.0)),
                    "descricao_situacao_cadastral": dados.get("situacao"),
                    "natureza_juridica": dados.get("natureza_juridica"),
                    "cnae_fiscal": dados.get("atividade_principal", [{}])[0].get("code", "").replace(".", "").replace("-", ""),
                    "cnae_fiscal_descricao": dados.get("atividade_principal", [{}])[0].get("text"),
                    "cnaes_secundarios": [{"codigo": c.get("code", "").replace(".", "").replace("-", ""), "descricao": c.get("text")} for c in dados.get("atividades_secundarias", [])],
                    "qsa": [{"nome_socio": s.get("nome"), "qualificacao_socio": s.get("qual")} for s in dados.get("qsa", [])]
                }
        except Exception:
            pass
    raise HTTPException(status_code=404, detail="CNPJ não localizado nas fontes federadas.")

async def notify_n8n(data: dict):
    """Disparo assíncrono para o barramento n8n."""
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            await client.post(MCP_SERVERS["n8n_bridge"], json=data)
    except Exception:
        pass

def processar_matriz_cognitiva(cnae_principal: str, cnaes_secundarios: list, capital_social: float, natureza_juridica: str, is_cpf: bool = False) -> dict:
    """Core Engine: Matriz de Teses Fiscais e Jurídicas."""
    all_cnaes = [cnae_principal] + [c['codigo'] for c in cnaes_secundarios]
    scores = {"inovacao": 4.0, "tributario": 5.0, "funding": 5.0, "export": 2.0}
    oportunidades = {
        "modulo_fiscal": [], "modulo_fomento_editais": [], "modulo_juridico_rj": [], "modulo_terceiro_sector": [], "comercio_exterior": []
    }

    if is_cpf:
        scores["tributario"] = 8.5
        oportunidades["modulo_fiscal"].append("Simulação de Carnê-Leão vs. Pejotização.")
        oportunidades["modulo_juridico_rj"].append("Estruturação de Holding Familiar.")
        return {"scores": scores, "oportunidades": oportunidades}

    # Gatilhos de Porte e Natureza
    if "213-5" in natureza_juridica or capital_social <= 20000.00:
        oportunidades["modulo_juridico_rj"].append("Gatilho de Transição MEI para ME.")

    for cnae in all_cnaes:
        prefix = cnae[:2]
        if prefix in ["56", "47"]:
            scores["tributario"] = max(scores["tributario"], 9.0)
            oportunidades["modulo_fiscal"].append("Recuperação PIS/COFINS Monofásico.")
        elif prefix in ["28", "29", "30", "25", "10", "86"]:
            scores["tributario"] = max(scores["tributario"], 9.5)
            oportunidades["modulo_fiscal"].append("Tese ICMS TUST/TUSD.")
        
        if prefix in ["62", "63", "20"]:
            scores["inovacao"] = max(scores["inovacao"], 9.5)
            oportunidades["modulo_fomento_editais"].append("Lei do Bem (P&D).")

    return {"scores": scores, "oportunidades": oportunidades}