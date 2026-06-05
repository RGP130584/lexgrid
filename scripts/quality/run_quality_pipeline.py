import subprocess
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("QualityPipeline")

def run_script(script_path: Path):
    logger.info(f"--- Executando Validador: {script_path.name} ---")
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        logger.error(f"Falha no fluxo de qualidade: {script_path.name}")
        return False
    return True

def main():
    logger.info("=== INICIANDO PIPELINE DE QUALIDADE (LEXGRID CAMADA 1) ===")
    quality_dir = Path(__file__).parent
    
    scripts_to_run = [
        quality_dir / "validate_env.py",
        quality_dir / "validate_imports.py",
        quality_dir / "validate_architecture.py",
        quality_dir / "ai_code_guard.py",
        quality_dir / "quick_smoke_tests.py"
    ]
    
    for script in scripts_to_run:
        if script.exists() and not run_script(script):
            logger.error("Commit interrompido. Resolva os problemas e tente novamente.")
            sys.exit(1)
    logger.info("=== QUALIDADE APROVADA ===")
    sys.exit(0)

if __name__ == "__main__":
    main()
