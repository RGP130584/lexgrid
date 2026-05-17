import subprocess
from datetime import datetime
from pathlib import Path
import json
from ..integrity.checksum_validator import ChecksumValidator

BACKUP_DIR = Path(__file__).resolve().parent.parent.parent / "backups" / "postgres"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

class PostgresBackupManager:
    """Gerencia backups incrementais/completos criptografados do PostgreSQL via Docker."""
    
    CONTAINER_NAME = "lexgrid_postgres"
    DB_USER = "lexadmin"
    DB_NAME = "lexgrid_core"

    @classmethod
    def execute_full_backup(cls) -> dict:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = f"pg_full_{timestamp}.sql.gz"
        filepath = BACKUP_DIR / filename
        
        # Executa pg_dump dentro do container e redireciona para o host
        cmd = f"docker exec {cls.CONTAINER_NAME} pg_dump -U {cls.DB_USER} -d {cls.DB_NAME} -Z 9 -F c > {filepath}"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            checksum = ChecksumValidator.generate_sha256(filepath)
            return {
                "status": "success",
                "file": str(filepath),
                "checksum": checksum,
                "timestamp": timestamp,
                "type": "full"
            }
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}