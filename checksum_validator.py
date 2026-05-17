import hashlib
from pathlib import Path

class ChecksumValidator:
    """Valida integridade de Backups, Snapshots e Configurações."""
    
    @staticmethod
    def generate_sha256(filepath: Path) -> str:
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado para checksum: {filepath}")
            
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def verify_integrity(filepath: Path, expected_hash: str) -> bool:
        """Retorna True se o arquivo não estiver corrompido ou adulterado."""
        actual_hash = ChecksumValidator.generate_sha256(filepath)
        return actual_hash == expected_hash