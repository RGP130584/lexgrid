import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LexGrid MVP - CNPJ Enrichment"
    VERSION: str = "1.0.0"
    REDIS_HOST: str = os.getenv("DRAGONFLY_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("DRAGONFLY_PORT", 56379))
    REDIS_PASSWORD: str = os.getenv("DRAGONFLY_PASSWORD", "dragonfly_secure_pass")
    RECEITA_API_URL: str = "https://brasilapi.com.br/api/cnpj/v1"
    RECEITA_WS_URL: str = "https://receitaws.com.br/v1/cnpj"
    
    class Config:
        env_file = ".env"

settings = Settings()