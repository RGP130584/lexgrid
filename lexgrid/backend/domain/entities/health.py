from pydantic import BaseModel

class SystemStatus(BaseModel):
    status: str
    system: str
    version: str
