from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
import re

class CNAE(BaseModel):
    codigo: str
    descricao: str

class DiagnosticResult(BaseModel):
    identificador: str
    tipo: str
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    capital_social: float = 0.0
    situacao: Optional[str] = None
    natureza_juridica: Optional[str] = None
    cnae_principal: Optional[CNAE] = None
    cnaes_secundarios: List[CNAE] = []
    qsa: List[str] = []
    scoring_estrategico: Dict[str, float]
    oportunidades_mapeadas: Dict[str, List[str]]
    divida_ativa_uniao: List[str] = []
    fontes_nao_oficiais: Dict[str, Any] = {}
    fonte_dados_mcp: Optional[str] = None
    status_infraestrutura: Dict[str, str] = {
        "mcp_protocol": "ACTIVE",
        "rag_status": "ONLINE",
        "llm_local": "READY"
    }

class DiagnosticoRequest(BaseModel):
    identificador: str

    @field_validator('identificador')
    @classmethod
    def validar_e_sanitizar(cls, v: str) -> str:
        limpo = re.sub(r'\D', '', v)
        if len(limpo) not in [11, 14]:
            raise ValueError('O identificador deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos).')
        return limpo