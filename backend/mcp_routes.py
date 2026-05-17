from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ToolCallRequest(BaseModel):
    tool_name: str
    parameters: dict

@router.get("/tools")
def list_mcp_tools():
    """
    MCP (Model Context Protocol) - Gateway
    Expõe o dicionário de ferramentas (capabilities) disponíveis para os Agentes LLM.
    """
    return {
        "mcp_version": "1.0",
        "tools": [
            {
                "name": "consultar_sped_historico",
                "description": "Consulta os metadados de arquivos SPED ingeridos na base relacional do LexGrid.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Nome do arquivo (ex: sped_janeiro.txt)"}
                    },
                    "required": ["filename"]
                }
            }
        ]
    }

@router.post("/tools/call")
def call_mcp_tool(request: ToolCallRequest):
    """Endpoint chamado pelos agentes de IA para executar a ferramenta escolhida."""
    if request.tool_name == "consultar_sped_historico":
        filename = request.parameters.get("filename")
        if not filename:
            return {"status": "error", "message": "O parâmetro 'filename' é obrigatório para consultar o histórico."}

        # TODO: Implementar a conexão com o banco 'lexgrid_postgres' via Repositório para busca real.
        return {
            "status": "success",
            "content": f"Histórico recuperado para o arquivo '{filename}': O registro foi localizado na base relacional e está pronto para análise."
        }
    
    return {"status": "error", "message": "Ferramenta não registrada no MCP Gateway."}