import os
from pathlib import Path
import logging

logger = logging.getLogger("PurgeManager")

class PurgeManager:
    """Destruição Segura de Dados e Arquivos (Zeroing/Overwriting)."""
    
    @staticmethod
    def secure_delete(filepath: Path, passes: int = 3):
        """Sobrescreve o arquivo com bytes aleatórios antes de deletar."""
        if not filepath.exists():
            return False
            
        length = filepath.stat().st_size
        logger.info(f"Executando exclusão segura ({passes} passes) em: {filepath.name}")
        
        with open(filepath, "r+b") as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
                os.fsync(f.fileno())
                
        filepath.unlink()
        return True