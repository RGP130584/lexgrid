import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from .config import LOGS_DIR, REPORTS_DIR

LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

class Observability:
    def __init__(self):
        self.run_id = str(uuid.uuid4())[:8]
        self.logger = logging.getLogger(f"Zelador-{self.run_id}")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s')
            fh = logging.FileHandler(LOGS_DIR / "zelador_layer2.log", encoding="utf-8")
            fh.setFormatter(formatter)
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def generate_report(self, data: dict):
        report_path = REPORTS_DIR / "diagnostic_report.json"
        payload = {
            "run_id": self.run_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
        self.logger.info(f"Relatório de Diagnóstico gerado: {report_path}")