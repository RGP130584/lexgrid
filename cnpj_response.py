from pydantic import BaseModel
from typing import List, Dict, Optional
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
    tax_profile: TaxProfile
    eligible_domains: List[str] = []
    potential_opportunities: List[str] = []
    risk_flags: List[str] = []
    scores: Dict[str, str]