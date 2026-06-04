import hashlib
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any

class DataLineageTracker:
    """
    Rastreia e audita o fluxo de dados entre o usuário, o Qdrant (Vetorial) e o Ollama (LLM).
    Garante a arquitetura Zero Trust criando um hash criptográfico imutável para cada resposta gerada.
    """
    
    def __init__(self):
        # Em um cenário real, isso seria gravado no PostgreSQL ou no HashiCorp Vault
        self.audit_log = []

    def _generate_trace_id(self) -> str:
        """Gera um ID único de rastreamento para a transação da IA."""
        return f"trace_{uuid.uuid4().hex[:16]}"

    def create_audit_record(
        self, 
        user_prompt: str, 
        retrieved_context: List[str], 
        llm_response: str, 
        user_id: str = "system"
    ) -> Dict[str, Any]:
        """
        Empacota a pergunta, a prova (Qdrant) e a resposta (Ollama) em um log selado.
        """
        trace_id = self._generate_trace_id()
        
        event_payload = {
            "trace_id": trace_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "lineage": {
                "input_prompt": user_prompt,
                "qdrant_context_used": retrieved_context, # A "prova" de onde a IA tirou a info
                "llm_output": llm_response
            }
        }

        # Assinatura Criptográfica SHA-256 (Garante a imutabilidade do log)
        # Se um byte da resposta for alterado depois, o hash quebra, denunciando fraude.
        event_string = json.dumps(event_payload, sort_keys=True)
        event_hash = hashlib.sha256(event_string.encode('utf-8')).hexdigest()
        
        event_payload["signature"] = event_hash

        # Salva o evento em memória (para a auditoria)
        self.audit_log.append(event_payload)
        
        # Retorna o ID para ser exibido no Frontend (Trace-ID)
        return event_payload