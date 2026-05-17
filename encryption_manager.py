import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class EncryptionManager:
    """Criptografia em repouso e de campos para LGPD compliance."""
    
    @classmethod
    def _get_master_key(cls) -> bytes:
        # Em produção, essa chave vem do HashiCorp Vault Transit Engine
        key_b64 = os.getenv("MASTER_ENCRYPTION_KEY", "uE2aB+x2vK9P2JtW2vGgTq9G/QkC+vE6Uv2y3C4R1Qc=")
        return base64.b64decode(key_b64)

    @classmethod
    def encrypt_field(cls, data: str) -> str:
        """Criptografa um dado sensível (CPF, RG) com AES-GCM (Autenticado)."""
        aesgcm = AESGCM(cls._get_master_key())
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, data.encode('utf-8'), None)
        return base64.b64encode(nonce + ct).decode('utf-8')

    @classmethod
    def decrypt_field(cls, token: str) -> str:
        """Descriptografa um dado sensível."""
        aesgcm = AESGCM(cls._get_master_key())
        raw_token = base64.b64decode(token.encode('utf-8'))
        nonce = raw_token[:12]
        ct = raw_token[12:]
        data = aesgcm.decrypt(nonce, ct, None)
        return data.decode('utf-8')