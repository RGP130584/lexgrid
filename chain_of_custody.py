import hashlib
import json
from datetime import datetime
from pathlib import Path

FORENSICS_DIR = Path(__file__).resolve().parent.parent / "audit" / "forensics"
FORENSICS_DIR.mkdir(parents=True, exist_ok=True)

class ChainOfCustody:
    """Garante imutabilidade de evidências digitais através de Hashing Criptográfico."""
    
    @staticmethod
    def generate_hash(filepath: Path) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def register_evidence(filepath: Path, handler: str, description: str) -> str:
        file_hash = ChainOfCustody.generate_hash(filepath)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "handler": handler,
            "evidence_file": filepath.name,
            "sha256_hash": file_hash,
            "description": description
        }
        log_file = FORENSICS_DIR / "custody_chain.jsonl"
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
        return file_hash