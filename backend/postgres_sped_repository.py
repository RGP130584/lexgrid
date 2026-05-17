import psycopg2
import json
import os
from domain.entities.sped import SpedFile
from domain.repositories.sped_repository import SpedRepository
from vault import vault_manager


class PostgresSpedRepository(SpedRepository):
    def __init__(self):
        # Busca a senha diretamente da RAM do Vault (Segurança Fiduciária)
        db_password = vault_manager.get_secret(path='database', key='password')
        
        # Fallback para variáveis de ambiente caso o Vault não esteja provisionado
        if not db_password:
            db_password = os.getenv("POSTGRES_PASSWORD", "lexpassword_secure_2026")

        # As credenciais espelham a configuração do docker-compose.yml
        self.conn_kwargs = {
            "dbname": "lexgrid_core",
            "user": "lexadmin",
            "password": db_password,
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", "55433")
        }
        self._init_db()

    def _init_db(self):
        """Garante que a tabela exista (Mecanismo simplificado para Fase 2)"""
        with psycopg2.connect(**self.conn_kwargs) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sped_files (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255),
                        file_type VARCHAR(100),
                        records_count INT,
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()

    def save(self, sped_file: SpedFile) -> bool:
        with psycopg2.connect(**self.conn_kwargs) as conn:
            with conn.cursor() as cur:
                records_json = json.dumps([r.data for r in sped_file.records])
                cur.execute(
                    """
                    INSERT INTO sped_files (filename, file_type, records_count, raw_data)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (sped_file.filename, sped_file.file_type, len(sped_file.records), records_json)
                )
            conn.commit()
        return True