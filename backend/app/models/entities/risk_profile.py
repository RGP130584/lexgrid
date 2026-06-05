from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RiskProfile(BaseModel):
    score_global: float
    score_financeiro: float
    score_compliance: float
    score_cibernetico: float
    score_mercado: float
    antecedentes_criminais: List[Dict[str, Any]] = []
    mandados_prisao: List[Dict[str, Any]] = []
    processos_judiciais: List[Dict[str, Any]] = []
    vulnerabilidades_ciberneticas: List[Dict[str, Any]] = []
    protestos: List[Dict[str, Any]] = []
    swot: Dict[str, List[str]] = {
        "forcas": [],
        "fraquezas": [],
        "oportunidades": [],
        "ameacas": []
    }
    parecer_mitigacao: str
