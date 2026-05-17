import hashlib
from datetime import datetime
from typing import Dict, Any

class PromptGovernance:
    """Controle de Versionamento e Aprovação de Prompts (Prompt-as-Code)."""
    
    # Mock in-memory para armazenamento de prompts
    _prompts_db = {}

    @classmethod
    def create_prompt(cls, name: str, template: str, owner: str, criticality: str) -> str:
        version = "1.0.0"
        prompt_hash = hashlib.sha256(template.encode()).hexdigest()
        
        cls._prompts_db[f"{name}@{version}"] = {
            "name": name,
            "version": version,
            "template": template,
            "hash": prompt_hash,
            "owner": owner,
            "criticality": criticality,
            "status": "DRAFT",
            "created_at": datetime.utcnow().isoformat()
        }
        return version

    @classmethod
    def approve_prompt(cls, name: str, version: str, approver: str):
        prompt = cls._prompts_db.get(f"{name}@{version}")
        if not prompt:
            raise ValueError("Prompt não encontrado.")
        
        if prompt["criticality"] in ["HIGH", "CRITICAL"] and approver == prompt["owner"]:
            raise PermissionError("Separação de funções violada: Owner não pode aprovar prompt crítico.")
            
        prompt["status"] = "APPROVED"
        prompt["approved_by"] = approver
        prompt["approved_at"] = datetime.utcnow().isoformat()