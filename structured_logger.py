import logging
import json
from datetime import datetime
from pathlib import Path
from .correlation import get_correlation_id
from .sanitizer import LogSanitizer

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "audit"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class StructuredJSONFormatter(logging.Formatter):
    """Formatter customizado gerando saídas em JSON puro para ingestão no SIEM."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
        }
        
        if hasattr(record, "extra_info") and isinstance(record.extra_info, dict):
            log_record["context"] = LogSanitizer.sanitize_dict(record.extra_info)
            
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def get_structured_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(f"lexgrid.{name}")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Console Handler
        ch = logging.StreamHandler()
        ch.setFormatter(StructuredJSONFormatter())
        logger.addHandler(ch)
        
        # File Handler Imutável (Append Only)
        log_file = LOG_DIR / "structured_audit.jsonl"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(StructuredJSONFormatter())
        logger.addHandler(fh)
        
    return logger