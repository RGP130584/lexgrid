"""
SCRIPT DEPRECIADO.
A pipeline de qualidade (Camada 1) foi modularizada e profissionalizada.
A execução agora é gerenciada estritamente pelo arquivo .pre-commit-config.yaml
e orquestrada pelos arquivos na pasta scripts/quality/.
"""
import sys

def main():
    print("\n" + "="*60)
    print("❌ SCRIPT DEPRECIADO: pre-commit-hook.py")
    print("="*60)
    print("A pipeline de qualidade (Camada 1) foi modularizada e profissionalizada.")
    print("A execução agora é gerenciada pelo .pre-commit-config.yaml.")
    print("Por favor, atualize seus hooks do git com os seguintes comandos:")
    print("    pip install pre-commit")
    print("    pre-commit install")
    print("="*60 + "\n")
    sys.exit(1)

if __name__ == "__main__":
    main()
