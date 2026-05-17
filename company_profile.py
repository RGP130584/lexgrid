from pydantic import BaseModel
from typing import List, Optional, Dict
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
    qsa: List[Dict[str, str]] = []