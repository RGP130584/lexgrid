import sys
import os
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ValidateEnv")

def main():
    logger.info("Auditando arquivos de variáveis de ambiente (.env)...")
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'password=' in content.lower() or 'secret=' in content.lower():
                logger.warning("ALERTA: Possível exposição de credenciais em plain text no .env detectada.")
                
    logger.info("[OK] Validação de ambiente estático concluída.")
    sys.exit(0)

if __name__ == "__main__":
    main()