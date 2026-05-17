from typing import Dict, Any

class ABACEngine:
    """Attribute-Based Access Control para tomada de decisão granular."""
    
    @staticmethod
    def is_allowed(subject: Dict[str, Any], resource: str, action: str, context: Dict[str, Any]) -> bool:
        role = subject.get("role", "guest")
        clearance = subject.get("clearance_level", 0)
        resource_sensitivity = context.get("resource_sensitivity", 0)
        
        # Regra 1: Separação de IA e Segredos (IA NUNCA acessa Vault/Secrets)
        if subject.get("is_ai") and "secret" in resource.lower():
            return False
            
        # Regra 2: Least Privilege de Sensibilidade
        if clearance < resource_sensitivity:
            return False
            
        # Regra 3: Escopo do Serviço
        if role == "database_service" and action != "read_write_db":
            return False
            
        return True