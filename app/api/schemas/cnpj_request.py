from pydantic import BaseModel, field_validator
from app.utils.validators import validate_cnpj

class CNPJRequest(BaseModel):
    cnpj: str

    @field_validator("cnpj")
    @classmethod
    def check_cnpj(cls, v: str) -> str:
        clean = v.replace(".", "").replace("/", "").replace("-", "").strip()
        if not validate_cnpj(clean):
            raise ValueError("CNPJ inválido.")
        return clean
