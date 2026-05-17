import json
from pathlib import Path
from datetime import datetime

COST_REPORT_FILE = Path(__file__).resolve().parent.parent.parent / "reports" / "ai_cost_report.json"
COST_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

class AICostTracker:
    """Monitoramento de Custos e FinOps para IA Operacional."""
    
    # Tabela de Custos Hipotética (On-Premise = Custo Energético/Hardware ou API externa)
    COST_PER_1K_TOKENS = {
        "lexgrid-core-7b": 0.0001,
        "lexgrid-embedding-v1": 0.00002,
        "fallback-cloud-api": 0.0020
    }

    @classmethod
    def register_usage(cls, model_id: str, tokens: int, environment: str = "prod"):
        cost_rate = cls.COST_PER_1K_TOKENS.get(model_id, 0.001)
        estimated_cost = (tokens / 1000.0) * cost_rate
        
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model_id": model_id,
            "environment": environment,
            "tokens_consumed": tokens,
            "estimated_cost_usd": estimated_cost
        }
        
        # Append-only file approach for simplicity
        with open(COST_REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")