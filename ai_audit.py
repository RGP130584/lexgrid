import json
import logging
from datetime import datetime
from pathlib import Path

AUDIT_FILE = Path(__file__).resolve().parent.parent.parent / "audit" / "ai_audit.log"
AUDIT_FILE.parent.mkdir(exist_ok=True)

logger = logging.getLogger("AIAudit")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(AUDIT_FILE, encoding='utf-8')
fh.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(fh)

class AIAudit:
    """Gera trilha de auditoria fiduciária para todas as interações do LLM."""
    
    @classmethod
    def log_interaction(cls, user_id: str, prompt: str, response: str, model: str, blocked: bool, reason: str = ""):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "model": model,
            "action_blocked": blocked,
            "block_reason": reason,
            "prompt_length": len(prompt),
            "response_length": len(response),
            # Em modo compliance, o prompt original não deve ser logado se contiver PII
            "prompt_hash": hash(prompt) 
        }
        logger.info(json.dumps(entry))