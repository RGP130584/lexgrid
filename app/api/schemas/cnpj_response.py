from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from app.models.value_objects.cnae import CNAE
from app.models.value_objects.tax_profile import TaxProfile

class CNPJResponse(BaseModel):
    cnpj: str
    company_name: str
    trade_name: Optional[str] = None
    segment: str
    state: str
    city: str
    company_size: str
    main_cnae: CNAE
    secondary_cnaes: List[CNAE] = []
    qsa: List[Dict[str, Any]] = []
    capital_social: float = 0.0
    divida_ativa_uniao: List[Dict[str, Any]] = []
    fomentos_nao_reembolsaveis: List[Dict[str, Any]] = []
    regime_simulacao: Dict[str, Any] = {}
    reducao_tributaria: List[Dict[str, Any]] = []
    reforma_tributaria: Dict[str, Any] = {}
    incentivos_inovacao: List[Dict[str, Any]] = []
    fontes_consultadas: List[Dict[str, Any]] = []
    tax_profile: TaxProfile
    eligible_domains: List[str] = []
    potential_opportunities: List[str] = []
    risk_flags: List[str] = []
    scores: Dict[str, str]