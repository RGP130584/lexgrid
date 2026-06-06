from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from app.services.llm_adapter import execute_ai_tool
from app.core.security.rate_limit import check_ai_rate_limit, beta_access_bypass
import json

router = APIRouter(dependencies=[Depends(check_ai_rate_limit), Depends(beta_access_bypass)])

class AnalyzeRiskRequest(BaseModel):
    cnpjData: Dict[str, Any] = Field(..., description="Dados cadastrais e gerais do CNPJ")
    riscosMapeados: Dict[str, Any] = Field(default_factory=dict, description="Riscos identificados no chassi")

class GenerateSWOTRequest(BaseModel):
    cnpjData: Dict[str, Any] = Field(..., description="Dados cadastrais e gerais do CNPJ")
    riscosMapeados: Dict[str, Any] = Field(..., description="Riscos identificados no chassi")

class ExtractNCMRequest(BaseModel):
    text: str = Field(..., description="Texto bruto ou conteúdo da nota fiscal para extração de NCM")


@router.post("/analyze-risk")
async def analyze_risk(payload: AnalyzeRiskRequest):
    """
    TOOL: Análise de Risco Corporativo e Auditoria
    Recebe dados cadastrais e financeiros e gera uma pontuação de risco inteligente com parecer analítico.
    """
    system_prompt = (
        "Você é um Analista de Risco de Crédito e Conformidade Sênior.\n"
        "Sua tarefa é analisar os dados financeiros e cadastrais fornecidos e classificar o risco geral da empresa.\n"
        "Retorne OBRIGATORIAMENTE um objeto JSON válido contendo exatamente os seguintes campos:\n"
        "{\n"
        "  \"score_risk\": <número de 0 a 100, onde 100 é o melhor cenário/sem risco>,\n"
        "  \"criticidade\": <string contendo 'baixo', 'medio', 'alto' ou 'critico'>,\n"
        "  \"analise\": <justificativa analítica fundamentada sobre os fatores de risco e mitigação sugerida>\n"
        "}\n"
        "Não escreva nada fora do JSON."
    )

    user_payload = (
        f"DADOS DA EMPRESA: {json.dumps(payload.cnpjData)}\n"
        f"RISCOS MAPEADOS: {json.dumps(payload.riscosMapeados)}"
    )

    try:
        result = await execute_ai_tool(system_prompt, user_payload, require_json=True)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-swot")
async def generate_swot(payload: GenerateSWOTRequest):
    """
    TOOL: Gerador de Matriz SWOT Tributária/Empresarial
    Recebe dados cadastrais e riscos mapeados e gera os quadrantes da SWOT.
    """
    system_prompt = (
        "Você é um Consultor Sênior de Risco Empresarial e Especialista Tributário.\n"
        "Sua tarefa é receber os dados mapeados de um CNPJ e classificar os cenários em uma Matriz SWOT clássica.\n"
        "Você DEVE retornar a resposta OBRIGATORIAMENTE em formato JSON com a seguinte estrutura exata:\n"
        "{\n"
        "   \"forces\": [\"lista de forças internas\"],\n"
        "   \"weaknesses\": [\"lista de fraquezas internas\"],\n"
        "   \"opportunities\": [\"lista de oportunidades externas tributárias/mercado\"],\n"
        "   \"threats\": [\"lista de ameaças macroeconômicas ou fiscais\"]\n"
        "}\n"
        "Não inclua nenhum texto antes ou depois do JSON."
    )

    user_payload = (
        f"DADOS DA EMPRESA: {json.dumps(payload.cnpjData)}\n"
        f"RISCOS MAPEADOS NO SISTEMA: {json.dumps(payload.riscosMapeados)}"
    )

    try:
        result = await execute_ai_tool(system_prompt, user_payload, require_json=True)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-ncm")
async def extract_ncm(payload: ExtractNCMRequest):
    """
    TOOL: Extrator Semântico de NCM (Nomenclatura Comum do Mercosul)
    Lê o conteúdo bruto de texto ou notas fiscais e extrai os itens com seus respectivos códigos tributários NCM.
    """
    system_prompt = (
        "Você é um especialista tributário e classificador fiscal de NCM (Nomenclatura Comum do Mercosul).\n"
        "Sua tarefa é analisar o texto ou nota fiscal fornecida e extrair os produtos/serviços e seus respectivos códigos NCM de 8 dígitos.\n"
        "Retorne OBRIGATORIAMENTE um JSON contendo uma lista de itens com a seguinte estrutura:\n"
        "{\n"
        "  \"items\": [\n"
        "     {\n"
        "        \"produto\": \"nome ou descrição detalhada do produto\",\n"
        "        \"ncm\": \"código NCM formatado com 8 dígitos (ex: 84713012) ou null se não identificado\",\n"
        "        \"justificativa\": \"breve fundamentação legal ou técnica da classificação\"\n"
        "     }\n"
        "  ]\n"
        "}\n"
        "Não escreva nada fora do JSON."
    )

    try:
        result = await execute_ai_tool(system_prompt, payload.text, require_json=True)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
