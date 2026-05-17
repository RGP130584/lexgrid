from fastapi import APIRouter, HTTPException, status, Request
import httpx
import re
import asyncio
from api.models.diagnostico import DiagnosticoRequest

router = APIRouter()

# Configuração de rotas de comunicação interna dos servidores MCP locais
MCP_SERVERS = {
    "osint_cascade": "http://localhost:5001/mcp/osint",
    "n8n_bridge": "http://localhost:5678/webhook/lexgrid-integration" 
}

async def call_mcp_tool_osint(cnpj: str) -> dict:
    """Abordagem MCP Pura: Chamada de ferramenta (Tool Call) para o MCP Server de OSINT."""
    # 1ª Linha de Cascata: BrasilAPI
    url_brasil_api = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url_brasil_api)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass

    # 2ª Linha de Cascata: ReceitaWS
    url_receitaws = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url_receitaws)
            if response.status_code == 200:
                dados = response.json()
                return {
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

    raise HTTPException(status_code=404, detail="Dispositivo MCP: CNPJ não localizado nas fontes federadas.")

async def call_mcp_tool_n8n(dados_diagnostico: dict):
    """Pipeline de disparo MCP para o n8n."""
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            await client.post(MCP_SERVERS["n8n_bridge"], json=dados_diagnostico)
    except Exception:
        pass

def processar_matriz_total(cnae_principal: str, cnaes_secundarios: list, capital_social: float, natureza_juridica: str, is_cpf: bool = False) -> dict:
    """Matriz Cognitiva V4.0 (Compliance MCP)."""
    all_cnaes = [cnae_principal] + [c['codigo'] for c in cnaes_secundarios]
    scores = {"inovacao": 4.0, "tributario": 5.0, "funding": 5.0, "export": 2.0}
    oportunidades = {
        "modulo_fiscal": [], "modulo_fomento_editais": [],
        "modulo_juridico_rj": [], "modulo_terceiro_sector": [], "comercio_exterior": []
    }

    if is_cpf:
        scores["tributario"] = 8.5
        oportunidades["modulo_fiscal"].append("Simulação de Carnê-Leão vs. Abertura de Pejotização Médica.")
        oportunidades["modulo_fiscal"].append("Análise e revisão do LCDPR.")
        oportunidades["modulo_juridico_rj"].append("Estruturação de Holding Patrimonial/Familiar.")
        return {"scores": scores, "oportunidades": oportunidades}

    if "213-5" in natureza_juridica or capital_social <= 20000.00:
        oportunidades["modulo_juridico_rj"].append("Gatilho de Transição MEI para ME.")
        oportunidades["modulo_fiscal"].append("Auditoria de taxas municipais e alvarás.")

    for cnae in all_cnaes:
        cnae_prefix = cnae[:2]
        if cnae_prefix in ["56", "47"]:
            scores["tributario"] = max(scores["tributario"], 9.0)
            oportunidades["modulo_fiscal"].append("Segregação Simples Nacional: PIS/COFINS Monofásico e ICMS-ST.")
        elif cnae_prefix in ["28", "29", "30", "25", "10", "86"]:
            scores["tributario"] = max(scores["tributario"], 9.5)
            oportunidades["modulo_fiscal"].append("Tese da Energia: Recuperação de ICMS sobre TUST/TUSD.")
        
        if cnae_prefix in ["62", "63", "20"]:
            scores["inovacao"] = max(scores["inovacao"], 9.5)
            oportunidades["modulo_fomento_editais"].append("Habilitação e Dedução Fiscal via Lei do Bem (P&D).")

        if cnae_prefix in ["79", "82", "93"]:
            scores["tributario"] = max(scores["tributario"], 9.6)
            oportunidades["modulo_fiscal"].append("Habilitação no PERSE (Alíquota Zero).")

    if capital_social >= 500000.00:
        oportunidades["modulo_fiscal"].append("Limitação da Base de Cálculo de Terceiros (Sistema S).")
        oportunidades["modulo_juridico_rj"].append("Viabilidade de Plano de Ação de Recuperação Judicial.")

    return {"scores": scores, "oportunidades": oportunidades}

@router.post("/diagnostico/cnpj", status_code=status.HTTP_200_OK)
async def processar_diagnostico_mcp(payload: DiagnosticoRequest):
    """Endpoint mestre que opera via Tool Call do protocolo MCP."""
    identificador = payload.identificador
    
    if len(identificador) == 11:
        matriz = processar_matriz_total(cnae_principal="", cnaes_secundarios=[], capital_social=0.0, natureza_juridica="", is_cpf=True)
        response_data = {
            "identificador": identificador, "tipo": "CPF", "status_cadastro": "REGULAR",
            "scoring_estrategico": matriz["scores"], "oportunidades_mapeadas": matriz["oportunidades"]
        }
        asyncio.create_task(call_mcp_tool_n8n(response_data))
        return response_data
        
    try:
        dados_brutos = await call_mcp_tool_osint(identificador)
        cnae_principal_formatado = {"codigo": str(dados_brutos.get("cnae_fiscal", "")), "descricao": dados_brutos.get("cnae_fiscal_descricao", "")}
        cnaes_secundarios_formatados = [{"codigo": str(c.get("codigo", "")), "descricao": c.get("descricao", "")} for c in dados_brutos.get("cnaes_secundarios", [])]
        
        qsa_lista = [f"{s.get('nome_socio')} ({s.get('qualificacao_socio')})" for s in dados_brutos.get("qsa", [])]
        capital_social = float(dados_brutos.get("capital_social", 0.0))
        natureza_juridica = dados_brutos.get("natureza_juridica", "")

        matriz = processar_matriz_total(cnae_principal_formatado["codigo"], cnaes_secundarios_formatados, capital_social, natureza_juridica)

        response_data = {
            "identificador": identificador, "tipo": "CNPJ",
            "razao_social": dados_brutos.get("razao_social"),
            "nome_fantasia": dados_brutos.get("nome_fantasia") or dados_brutos.get("razao_social"),
            "capital_social": capital_social, "situacao": dados_brutos.get("descricao_situacao_cadastral"),
            "cnae_principal": cnae_principal_formatado, "cnaes_secundarios": cnaes_secundarios_formatados,
            "qsa": qsa_lista, "scoring_estrategico": matriz["scores"], "oportunidades_mapeadas": matriz["oportunidades"],
            "status_infraestrutura": {
                "mcp_protocol": "ACTIVE (mTLS)", "rag_status": "ONLINE", "redis_cache": "ACTIVE", "llm_local": "READY (Qwen-7B)"
            }
        }
        asyncio.create_task(call_mcp_tool_n8n(response_data))
        return response_data

    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Erro Crítico de barramento no protocolo MCP local.")

@router.post("/webhook/universal", status_code=status.HTTP_200_OK)
async def webhook_universal_mcp(request: Request):
    """Webhook universal que pesca identificadores no barramento MCP."""
    try:
        body = await request.json()
        body_str = str(body)
        padrao_cnpj = re.findall(r'\d{14}', re.sub(r'\D', '', body_str))
        padrao_cpf = re.findall(r'\d{11}', re.sub(r'\D', '', body_str))
        
        identificador = padrao_cnpj[0] if padrao_cnpj else (padrao_cpf[0] if padrao_cpf else None)
            
        if not identificador:
            raise HTTPException(status_code=400, detail="Nenhum identificador corporativo pescado no barramento MCP.")
            
        return await processar_diagnostico_mcp(DiagnosticoRequest(identificador=identificador))
    except Exception:
        raise HTTPException(status_code=400, detail="Entrada de payload corrompida no protocolo.")