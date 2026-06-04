from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.models.value_objects.cnae import CNAE

class CompanyProfile(BaseModel):
    cnpj: str
    company_name: str
    trade_name: Optional[str] = None
    natureza_juridica: str
    capital_social: float
    state: str
    city: str
    company_size: str
    situacao_cadastral: str
    main_cnae: CNAE
    secondary_cnaes: List[CNAE] = []
    qsa: List[Dict[str, Any]] = []
    divida_ativa_uniao: List[Dict[str, Any]] = []
    fomentos_nao_reembolsaveis: List[Dict[str, Any]] = []
    regime_simulacao: Dict[str, Any] = {}
    reducao_tributaria: List[Dict[str, Any]] = []
    reforma_tributaria: Dict[str, Any] = {}
    incentivos_inovacao: List[Dict[str, Any]] = []
    fontes_consultadas: List[Dict[str, Any]] = []