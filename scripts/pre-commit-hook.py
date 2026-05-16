#!/usr/bin/env python3
import subprocess
import sys
import os

# Definição de cores para o terminal (Estilo Dashboard)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[*] {message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}[✓] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}[X] {message}{Colors.ENDC}")

def run_check(cmd_list, step_name, allow_fail=False):
    print_step(f"Executando: {step_name}")
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{step_name} passou com sucesso.")
            return True
        else:
            print_error(f"Falha em: {step_name}")
            print(f"{Colors.WARNING}{result.stdout}{Colors.ENDC}")
            print(f"{Colors.FAIL}{result.stderr}{Colors.ENDC}")
            if not allow_fail:
                sys.exit(1)
            return False
    except FileNotFoundError:
        print_error(f"Comando não encontrado para {step_name}. Verifique se a ferramenta está instalada.")
        if not allow_fail:
            sys.exit(1)
        return False


def main():
    print(f"{Colors.HEADER}{Colors.BOLD}=== ESTEIRA DE SEGURANÇA MILITAR - LEXGRID ==={Colors.ENDC}")
    
    # 1. Paranoia de Cadeia de Suprimentos (Supply Chain Audit)
    # Verifica se alguma biblioteca baixada (ex: python-sped, FastAPI) tem malware conhecido.
    run_check(['pip-audit'], "Auditoria de Dependências (pip-audit)")

    # 2. Análise Estática de Segurança (SAST)
    # Escaneia o código Python em busca de injeções SQL, senhas hardcoded, etc.
    # Ignora a pasta de ambiente virtual (.venv) e foca no backend.
    run_check(['bandit', '-r', 'backend/', '-ll', '-ii'], "Scanner Anti-Vulnerabilidade (Bandit)")

    # 3. Validação de Banco de Dados e Infraestrutura
    # Testa as conexões mTLS e integridade do Postgres e Qdrant
    if os.path.exists('backend/test_db.py'):
        run_check([sys.executable, 'backend/test_db.py'], "Testes de Integridade do Banco de Dados")
    else:
        print(f"{Colors.WARNING}[!] Aviso: backend/test_db.py não encontrado. Pulando teste de BD.{Colors.ENDC}")

    # 4. Checagem Linter e Anti-Bloat (Ruff)
    run_check(['ruff', 'check', 'backend/'], "Auditoria de Código Limpo (Ruff)")

    # 5. Aprovação Fiduciária Manual
    print(f"\n{Colors.WARNING}{Colors.BOLD}=== APROVAÇÃO NECESSÁRIA ==={Colors.ENDC}")
    print("Todas as checagens automatizadas passaram.")
    print("Por favor, confirme a intenção de consolidação deste código no chassi do Lexgrid.")
    
    # Proteção para ambientes não-interativos (ex: VS Code GUI, GitKraken)
    if not sys.stdin.isatty():
        print_success("Ambiente não interativo detectado. Aprovando automaticamente via Bypass Fiduciário.")
        sys.exit(0)

    while True:
        choice = input(f"{Colors.BOLD}Sua escolha [a] Aprova / [c] Cancela / [r] Revisa: {Colors.ENDC}").strip().lower()
        
        if choice == 'a':
            print_success("Commit Aprovado e Consolidado no Lexgrid.")
            sys.exit(0)
        elif choice == 'c':
            print_error("Commit Cancelado pelo Usuário.")
            sys.exit(1)
        elif choice == 'r':
            print_step("Acesse a extensão ChatGPT Go para revisão e tente o commit novamente.")
            sys.exit(1)
        else:
            print("Opção inválida. Escolha 'a', 'c' ou 'r'.")


if __name__ == "__main__":
    main()
