import os
from pathlib import Path

def get_project_root() -> Path:
    """Retorna o caminho absoluto raiz do projeto."""
    return Path(__file__).parent.parent.parent.resolve()