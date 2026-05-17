import json
import uuid
from datetime import datetime
from pathlib import Path

LINEAGE_FILE = Path(__file__).resolve().parent.parent.parent / "reports" / "lineage_report.jsonl"
LINEAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

class DataLineageTracker:
    """Mapeia o ciclo de vida do dado (Ingestão -> Transformação -> Embedding -> IA)."""
    
    @classmethod
    def record_flow(cls, source_id: str, action: str, dest_id: str, actor: str, sensitivity: int):
        flow_id = str(uuid.uuid4())
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "flow_id": flow_id,
            "source": source_id,
            "destination": dest_id,
            "action": action, # ex: "vectorized", "anonymized", "ingested"
            "actor_id": actor,
            "sensitivity_level": sensitivity
        }
        
        with open(LINEAGE_FILE, "a", encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
            
        return flow_id