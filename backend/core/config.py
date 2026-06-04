from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LexGrid Core API"
    VERSION: str = "3.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Aqui futuramente você colocará as URLs dos bancos de dados

settings = Settings()