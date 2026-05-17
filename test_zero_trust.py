import pytest
from security.zero_trust.trust_engine import ZeroTrustEngine
from security.iam.abac import ABACEngine
from security.secrets.encryption_manager import EncryptionManager

def test_abac_blocks_ai_from_secrets():
    subject = {"is_ai": True, "role": "llm_agent"}
    resource = "vault/secret/api_keys"
    action = "read"
    context = {}
    
    assert not ABACEngine.is_allowed(subject, resource, action, context)

def test_zero_trust_engine_behavior_block():
    # Simula IA tentando um dump massivo do banco (Ameaça identificada)
    subject = {"is_ai": True, "role": "llm_agent"}
    resource = "internal_database"
    action = "dump"
    context = {}
    
    # Deve ser negado primariamente pelo score de risco do BehaviorAnalyzer (>80)
    allowed = ZeroTrustEngine.evaluate_access(subject, resource, action, context)
    assert allowed is False

def test_field_level_encryption_cycle():
    cpf_plano = "123.456.789-00"
    token_cifrado = EncryptionManager.encrypt_field(cpf_plano)
    assert token_cifrado != cpf_plano
    assert EncryptionManager.decrypt_field(token_cifrado) == cpf_plano