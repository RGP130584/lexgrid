import hvac
import os

class VaultManager:
    def __init__(self):
        self.client = hvac.Client(
            url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
            token=os.getenv("VAULT_TOKEN", "lexgrid_temp_dev_token")
        )

    def get_secret(self, path: str, key: str) -> str:
        """Recupera um segredo específico do Vault."""
        try:
            # No modo dev, usamos o mount 'secret/'
            read_response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return read_response['data']['data'].get(key)
        except Exception as e:
            print(f"[ERRO] Falha ao recuperar segredo do Vault: {e}")
            return None

    def set_db_credentials(self, password: str):
        """Helper para inicializar credenciais no ambiente de dev."""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path='database',
                secret=dict(password=password)
            )
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao injetar segredo no Vault: {e}")
            return False

# Singleton para uso em toda a aplicação
vault_manager = VaultManager()