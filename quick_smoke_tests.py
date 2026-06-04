import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from logger import get_logger

logger = get_logger("QuickSmokeTests")

def main():
    logger.info("Executando Smoke Tests Locais (Dry Run)...")
    try:
        import pydantic
        logger.info("[OK] Core libraries importadas com sucesso.")
    except ImportError as e:
        logger.error(f"Falha crítica no ambiente virtual: {e}")
        sys.exit(1)
    sys.exit(0)
if __name__ == "__main__":
    main()