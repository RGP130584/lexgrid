from .prompt_guard import PromptGuard
from .pii_guard import PIIGuard
from ..observability.ai_audit import AIAudit

class AIFirewall:
    """
    Orquestrador Zero Trust. 
    Intercepta I/O do LLM, aplicando políticas de Guardrails e Auditoria.
    """
    
    @classmethod
    def process_request(cls, user_id: str, raw_prompt: str, model_name: str = "lexgrid-core") -> str:
        """Fase 1: Interceptação de Entrada (Ingress)"""
        
        # 1. Validação de Injection/Jailbreak
        is_safe, reason = PromptGuard.analyze(raw_prompt)
        if not is_safe:
            AIAudit.log_interaction(user_id, raw_prompt, "", model_name, blocked=True, reason=reason)
            raise ValueError(f"AI Firewall Block: {reason}")
            
        # O prompt passa intacto para a engine
        return raw_prompt

    @classmethod
    def process_response(cls, user_id: str, original_prompt: str, raw_response: str, model_name: str = "lexgrid-core") -> str:
        """Fase 2: Interceptação de Saída (Egress)"""
        
        # 1. Detectar vazamentos críticos (Ex: Chaves AWS geradas pela IA)
        if PIIGuard.detect_leakage(raw_response):
            AIAudit.log_interaction(user_id, original_prompt, raw_response, model_name, blocked=True, reason="Vazamento de Segredo/PII Crítico")
            return "[BLOQUEADO PELO FIREWALL: O output continha dados sensíveis não autorizados]"
            
        # 2. Sanitização/Mascaramento (Redaction)
        safe_output = PIIGuard.mask_data(raw_response)
        
        # 3. Auditoria de sucesso
        AIAudit.log_interaction(user_id, original_prompt, safe_output, model_name, blocked=False)
        return safe_output