from fastapi import APIRouter, status, Request
import asyncio
import re
from api.models.diagnostico import DiagnosticoRequest
from osint_engine import call_mcp_tool_universal_master, processar_matriz_cognitiva, notify_n8n

router = APIRouter()

@router.post("/diagnostico/cnpj", status_code=status.HTTP_200_OK)
async def diagnostico_cnpj(payload: DiagnosticoRequest):
    identificador = payload.identificador
    
    if len(identificador) == 11:
        matriz = processar_matriz_cognitiva(cnae_principal="", cnaes_secundarios=[], capital_social=0.0, natureza_juridica="", is_cpf=True)
        response = {"identificador": identificador, "tipo": "CPF", "scoring_estrategico": matriz["scores"], "oportunidades_mapeadas": matriz["oportunidades"]}
        asyncio.create_task(notify_n8n(response))
        return response

    dados = await call_mcp_tool_universal_master(identificador)
    matriz = processar_matriz_cognitiva(
        dados.get("cnae_fiscal", ""),
        dados.get("cnaes_secundarios", []),
        dados.get("capital_social", 0.0),
        dados.get("natureza_juridica", "")
    )

    response = {
        "identificador": identificador, "tipo": "CNPJ",
        "razao_social": dados.get("razao_social"),
        "nome_fantasia": dados.get("nome_fantasia"),
        "capital_social": dados.get("capital_social"),
        "situacao": dados.get("descricao_situacao_cadastral"),
        "natureza_juridica": dados.get("natureza_juridica"),
        "cnae_principal": {"codigo": dados.get("cnae_fiscal"), "descricao": dados.get("cnae_fiscal_descricao")},
        "cnaes_secundarios": dados.get("cnaes_secundarios"),
        "qsa": [f"{s.get('nome_socio')} ({s.get('qualificacao_socio')})" for s in dados.get("qsa", [])],
        "scoring_estrategico": matriz["scores"],
        "oportunidades_mapeadas": matriz["oportunidades"]
    }
    asyncio.create_task(notify_n8n(response))
    return response

@router.post("/webhook/universal")
async def webhook_universal(request: Request):
    body = await request.json()
    body_str = str(body)
    cnpj = re.findall(r'\d{14}', re.sub(r'\D', '', body_str))
    cpf = re.findall(r'\d{11}', re.sub(r'\D', '', body_str))
    identificador = cnpj[0] if cnpj else (cpf[0] if cpf else None)
    return await diagnostico_cnpj(DiagnosticoRequest(identificador=identificador))