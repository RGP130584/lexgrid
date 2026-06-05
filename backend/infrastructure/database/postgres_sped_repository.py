import json
from domain.entities.sped import SpedFile
from domain.repositories.sped_repository import SpedRepository
from infrastructure.database.db_connection import get_db_connection
from infrastructure.database.setup import init_database


class PostgresSpedRepository(SpedRepository):
    def __init__(self):
        # Garante a inicializacao de todas as tabelas
        init_database()

    def save(self, sped_file: SpedFile) -> bool:
        with get_db_connection() as conn:
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
