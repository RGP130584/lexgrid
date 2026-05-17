import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

MODELS_DB_FILE = Path(__file__).resolve().parent.parent.parent / "models" / "registry.json"
MODELS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)

class ModelRegistry:
    """Registro Corporativo de Modelos de Inteligência Artificial (LLMs e Embeddings)."""
    
    @classmethod
    def _load_db(cls) -> Dict[str, Any]:
        if not MODELS_DB_FILE.exists():
            return {}
        with open(MODELS_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
            
    @classmethod
    def _save_db(cls, db: Dict[str, Any]):
        with open(MODELS_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

    @classmethod
    def register_model(cls, model_id: str, version: str, checksum: str, license_type: str, owner: str, risk_level: str):
        db = cls._load_db()
        db[f"{model_id}@{version}"] = {
            "model_id": model_id,
            "version": version,
            "checksum": checksum,
            "license": license_type,
            "owner": owner,
            "risk_level": risk_level,
            "approval_status": "PENDING_GATES",
            "registered_at": datetime.utcnow().isoformat() + "Z"
        }
        cls._save_db(db)

    @classmethod
    def get_approved_model(cls, model_id: str, version: str) -> Optional[Dict[str, Any]]:
        db = cls._load_db()
        model = db.get(f"{model_id}@{version}")
        if model and model.get("approval_status") == "APPROVED":
            return model
        return None