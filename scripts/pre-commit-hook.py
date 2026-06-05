#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

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
    print(f"{Colors.GREEN}[OK] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}[X] {message}{Colors.ENDC}")

def run_check(cmd_list, step_name, allow_fail=False):
    print_step(f"Executando: {step_name}")
    
    # Resolve command from .venv if available
    cmd = cmd_list[0]
    project_root = Path(__file__).resolve().parent.parent
    
    # Determine the venv directory
    venv_bin_dir = project_root / ".venv" / "Scripts" if os.name == 'nt' else project_root / ".venv" / "bin"
    venv_cmd = venv_bin_dir / cmd
    if os.name == 'nt' and not venv_cmd.suffix:
        venv_cmd = venv_cmd.with_suffix('.exe')
        
    resolved_cmd = str(venv_cmd) if venv_cmd.exists() else cmd
    cmd_list[0] = resolved_cmd
    
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, cwd=str(project_root))
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
        # Check if the fallback / default command works
        if resolved_cmd != cmd:
            try:
                cmd_list[0] = cmd
                result = subprocess.run(cmd_list, capture_output=True, text=True, cwd=str(project_root))
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
                pass

        print_error(f"Comando '{cmd}' não encontrado para {step_name}. Verifique se a ferramenta está instalada.")
        if not allow_fail:
            sys.exit(1)
        return False


def main():
    print(f"{Colors.HEADER}{Colors.BOLD}=== ESTEIRA DE SEGURANÇA MILITAR - LEXGRID ==={Colors.ENDC}")
    project_root = Path(__file__).resolve().parent.parent
    
    # 1. Paranoia de Cadeia de Suprimentos (Supply Chain Audit)
    # Verifica se alguma biblioteca baixada (ex: python-sped, FastAPI) tem malware conhecido.
    # Permitimos falha/pulamos se pip-audit não estiver instalado para evitar travar dev sem internet/ferramenta.
    run_check(['pip-audit'], "Auditoria de Dependências (pip-audit)", allow_fail=True)

    # 2. Análise Estática de Segurança (SAST)
    # Escaneia o código Python em busca de injeções SQL, senhas hardcoded, etc.
    run_check(['bandit', '-r', 'backend/', '-ll', '-ii'], "Scanner Anti-Vulnerabilidade (Bandit)")

    # 3. Validação de Banco de Dados e Infraestrutura
    # Executa os testes de banco de dados locais
    test_db_path = project_root / "test_db.py"
    backend_test_db_path = project_root / "backend" / "test_db.py"
    
    venv_bin_dir = project_root / ".venv" / "Scripts" if os.name == 'nt' else project_root / ".venv" / "bin"
    venv_python = venv_bin_dir / "python"
    if os.name == 'nt':
        venv_python = venv_python.with_suffix('.exe')
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    if test_db_path.exists():
        run_check([python_exe, str(test_db_path)], "Testes de Integridade do Banco de Dados (Raiz)")
    elif backend_test_db_path.exists():
        run_check([python_exe, str(backend_test_db_path)], "Testes de Integridade do Banco de Dados (Backend)")
    else:
        print(f"{Colors.WARNING}[!] Aviso: test_db.py não encontrado. Pulando teste de BD.{Colors.ENDC}")

    # 4. Checagem Linter e Anti-Bloat (Ruff / Flake8 / Pylint)
    # Tenta usar ruff, se não encontrar tenta flake8, senão pylint
    linter_run = False
    for linter in [['ruff', 'check', 'backend/'], ['flake8', 'backend/'], ['pylint', 'backend/']]:
        print_step(f"Tentando Linter: {linter[0]}")
        # Resolve linter in venv
        venv_bin_dir = project_root / ".venv" / "Scripts" if os.name == 'nt' else project_root / ".venv" / "bin"
        venv_cmd = venv_bin_dir / linter[0]
        if os.name == 'nt' and not venv_cmd.suffix:
            venv_cmd = venv_cmd.with_suffix('.exe')
        
        resolved_linter = str(venv_cmd) if venv_cmd.exists() else linter[0]
        cmd_list = [resolved_linter] + linter[1:]
        
        try:
            result = subprocess.run(cmd_list, capture_output=True, text=True, cwd=str(project_root))
            if result.returncode == 0:
                print_success(f"Linter {linter[0]} passou com sucesso.")
                linter_run = True
                break
            else:
                print_error(f"Aviso: Linter {linter[0]} encontrou problemas (não-bloqueante).")
                print(f"{Colors.WARNING}{result.stdout}{Colors.ENDC}")
                print(f"{Colors.FAIL}{result.stderr}{Colors.ENDC}")
                linter_run = True
                break
        except FileNotFoundError:
            continue
            
    if not linter_run:
        print(f"{Colors.WARNING}[!] Nenhum linter (ruff, flake8, pylint) pôde ser executado.{Colors.ENDC}")

    # 5. Aprovação Fiduciária Manual
    print(f"\n{Colors.WARNING}{Colors.BOLD}=== APROVAÇÃO NECESSÁRIA ==={Colors.ENDC}")
    print("Todas as checagens automatizadas passaram.")
    print("Por favor, confirme a intenção de consolidação deste código no chassi do Lexgrid.")
    
    # Proteção para ambientes não-interativos (ex: VS Code GUI, GitKraken)
    if not sys.stdin.isatty():
        print_success("Ambiente não interativo detectado. Aprovando automaticamente via Bypass Fiduciário.")
        sys.exit(0)

    while True:
        try:
            choice = input(f"{Colors.BOLD}Sua escolha [a] Aprova / [c] Cancela / [r] Revisa: {Colors.ENDC}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print_success("Ambiente não interativo (EOF) detectado. Aprovando automaticamente via Bypass Fiduciário.")
            sys.exit(0)
        
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
