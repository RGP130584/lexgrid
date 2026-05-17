import hvac
import os
from typing import Optional, Dict

class VaultManager:
    """Integração corporativa com HashiCorp Vault para rotação e armazenamento de segredos."""
    
    def __init__(self):
        vault_url = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
        vault_token = os.getenv("VAULT_TOKEN", "lexgrid_temp_dev_token")
        
        self.client = hvac.Client(
            url=vault_url,
            token=vault_token
        )

    def get_secret(self, path: str, key: str) -> Optional[str]:
        """Recupera um segredo sem armazená-lo em disco ou variáveis globais de longo prazo."""
        if not self.client.is_authenticated():
            raise PermissionError("Vault Client not authenticated.")
            
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response['data']['data'].get(key)
        except Exception as e:
            return None

    def rotate_secret(self, path: str, secrets_dict: Dict[str, str]):
        """Grava e rotaciona um segredo na Engine KV v2."""
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=secrets_dict
        )