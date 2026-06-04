import sys
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("QuickSmokeTests")

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