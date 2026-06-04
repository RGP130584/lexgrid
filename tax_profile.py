from pydantic import BaseModel

class TaxProfile(BaseModel):
    is_simples_nacional: bool
    presumed_profit_eligible: bool
    real_profit_eligible: bool
