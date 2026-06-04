import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from logger import get_logger

logger = get_logger("ValidateArchitecture")

def main():
    logger.info("Validando limites de arquitetura e acoplamento (Camada 1 vs Camada 2)...")
    project_root = Path(__file__).parent.parent.parent
    has_violation = False
    
    for py_file in (project_root / 'scripts').rglob('*.py'):
        if 'zelador' in py_file.parts:
            continue
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'from backend' in content or 'import backend' in content:
                    logger.error(f"Violação de acoplamento detectada em {py_file.relative_to(project_root)}. Scripts de automação não devem acoplar-se diretamente aos domínios do backend.")
                    has_violation = True
        except Exception:
            pass
    if has_violation:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()