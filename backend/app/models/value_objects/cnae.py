from pydantic import BaseModel

class CNAE(BaseModel):
    codigo: str
    descricao: str
