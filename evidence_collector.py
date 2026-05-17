import shutil
from pathlib import Path
from datetime import datetime
from .chain_of_custody import ChainOfCustody, FORENSICS_DIR

class EvidenceCollector:
    """Isola e empacota artefatos do sistema em caso de detecção de brechas."""
    
    @staticmethod
    def snapshot_logs(incident_id: str, handler: str):
        audit_dir = Path(__file__).resolve().parent.parent / "audit"
        snapshot_dir = FORENSICS_DIR / f"snapshot_{incident_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Copia todos os JSONL
        for log_file in audit_dir.glob("*.jsonl"):
            shutil.copy2(log_file, snapshot_dir)
            
        # Zipa o Snapshot
        archive_path = shutil.make_archive(str(snapshot_dir), 'zip', snapshot_dir)
        shutil.rmtree(snapshot_dir) # Remove RAW após zipar
        
        # Registra a evidência na cadeia de custódia
        archive_file = Path(archive_path)
        file_hash = ChainOfCustody.register_evidence(archive_file, handler, f"Log Snapshot for Incident {incident_id}")
        
        return archive_file, file_hash