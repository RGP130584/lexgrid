import psycopg2
import os
from core.vault import vault_manager

def get_db_connection():
    """Retorna uma conexao ativa com o banco PostgreSQL de acordo com o ambiente (Vault/ENV)."""
    db_password = vault_manager.get_secret(path='database', key='password')
    if not db_password:
        db_password = os.getenv("POSTGRES_PASSWORD", "lexpassword_secure_2026")
        
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "lexgrid_core"),
        user=os.getenv("POSTGRES_USER", "lexadmin"),
        password=db_password,
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "55433")
    )
