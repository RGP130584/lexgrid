import json
from datetime import datetime
from pathlib import Path
from ..prompt_attacks.injection_suite import PromptInjectionSuite
from ..rag_attacks.poisoning_tests import RAGPoisoningSuite
from ..simulations.ransomware_simulation import RansomwareSimulation
from ..chaos.service_failure import ChaosServiceFailure

REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class ResilienceValidator:
    """Orquestrador do Cyber Range: Executa todas as simulações ofensivas e gera Resilence Score."""
    
    @classmethod
    def execute_full_cyber_range(cls):
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "modules": {}
        }
        
        # 1. AI Red Team
        report["modules"]["prompt_injection"] = PromptInjectionSuite.run_tests()
        report["modules"]["rag_poisoning"] = RAGPoisoningSuite.simulate_attack()
        
        # 2. Infra Hardening
        report["modules"]["ransomware_immutability"] = {
            "postgres_protected": RansomwareSimulation.test_container_immutability("lexgrid_postgres"),
            "vault_protected": RansomwareSimulation.test_container_immutability("lexgrid_vault")
        }
        
        # Persiste resultado
        report_file = REPORTS_DIR / "resilience_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=4)
            
        return report