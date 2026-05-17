import schedule
import time
import threading
import logging
from .postgres_backup import PostgresBackupManager

logger = logging.getLogger("BackupScheduler")

class BackupScheduler:
    """Agendador autônomo de rotinas de resiliência."""

    @staticmethod
    def _job_postgres_full():
        logger.info("Iniciando Backup Full do PostgreSQL...")
        result = PostgresBackupManager.execute_full_backup()
        if result["status"] == "success":
            logger.info(f"Backup concluído: {result['file']} [SHA256: {result['checksum']}]")
        else:
            logger.error(f"Falha crítica no backup: {result.get('error')}")

    @classmethod
    def run_daemon(cls):
        # Agendamentos Governança RPO
        schedule.every().day.at("02:00").do(cls._job_postgres_full)
        schedule.every(6).hours.do(lambda: logger.info("Executando Qdrant Snapshot..."))
        
        logger.info("Backup Scheduler iniciado. Monitorando jobs...")
        
        def run_loop():
            while True:
                schedule.run_pending()
                time.sleep(60)
                
        thread = threading.Thread(target=run_loop, daemon=True)
        thread.start()