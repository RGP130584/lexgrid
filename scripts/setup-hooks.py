#!/usr/bin/env python3
"""
Setup script para instalar Git hooks da esteira LexGrid
Configura automaticamente validacoes pre-commit
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def setup_git_hooks():
    """Setup Git pre-commit hooks"""
    
    project_root = Path(__file__).resolve().parent.parent
    hooks_dir = project_root / ".git" / "hooks"
    
    if not hooks_dir.exists():
        print(f"[ERRO] Diretorio .git nao encontrado em {project_root}")
        print("Execute este script no diretorio raiz do projeto")
        return False
    
    # Create universal pre-commit hook (Git standard, works in Git Bash on Windows)
    pre_commit_sh = hooks_dir / "pre-commit"
    pre_commit_sh_content = f"""#!/bin/bash
# LexGrid Pre-Commit Hook (Universal)
cd "{project_root}"
python scripts/pre-commit-hook.py
exit $?
"""
    
    try:
        with open(pre_commit_sh, 'w', newline='\n') as f:
            f.write(pre_commit_sh_content)
        # Try to make it executable (important for UNIX/WSL, no-op usually on pure Windows)
        os.chmod(pre_commit_sh, 0o755)
        print(f"[OK] Git hook universal criado: {pre_commit_sh}")
    except Exception as e:
        print(f"[ERRO] Falha ao criar hook universal: {e}")
        return False

    # Create pre-commit hook (Windows batch version)
    pre_commit_bat = hooks_dir / "pre-commit.bat"
    pre_commit_bat_content = f"""@echo off
REM LexGrid Pre-Commit Hook
cd "{project_root}"
python scripts\\pre-commit-hook.py
exit /b %ERRORLEVEL%
"""
    
    try:
        with open(pre_commit_bat, 'w') as f:
            f.write(pre_commit_bat_content)
        print(f"[OK] Git hook instalado: {pre_commit_bat}")
    except Exception as e:
        print(f"[ERRO] Falha ao criar hook: {e}")
        return False
    
    # Also create PowerShell version
    pre_commit_ps1 = hooks_dir / "pre-commit.ps1"
    pre_commit_ps1_content = f"""# LexGrid Pre-Commit Hook
cd "{project_root}"
python scripts\\pre-commit-hook.py
exit $LASTEXITCODE
"""
    
    try:
        with open(pre_commit_ps1, 'w') as f:
            f.write(pre_commit_ps1_content)
        print(f"[OK] PowerShell hook criado: {pre_commit_ps1}")
    except Exception as e:
        print(f"[ERRO] Falha ao criar hook PS1: {e}")
        return False
    
    # Git require hook type configuration for Windows
    try:
        subprocess.run(
            f'git config core.hooksPath "{hooks_dir}"',
            shell=True,
            cwd=project_root,
            capture_output=True
        )
        print(f"[OK] Git configurado para usar hooks dinamicamente")
    except Exception as e:
        print(f"[AVISO] Falha ao configurar git hooks path: {e}")
    
    return True


def create_scripts_directory():
    """Ensure scripts directory exists"""
    scripts_dir = Path(__file__).resolve().parent
    scripts_dir.mkdir(exist_ok=True)
    print(f"[OK] Diretorio de scripts verificado: {scripts_dir}")
    return True


def verify_docker_containers():
    """Verify Docker is available"""
    try:
        result = subprocess.run(
            'docker --version',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[OK] Docker disponivel: {result.stdout.strip()}")
            return True
        else:
            print("[AVISO] Docker nao encontrado. Instale Docker Desktop para Windows.")
            return False
    except Exception as e:
        print(f"[AVISO] Erro ao verificar Docker: {e}")
        return False


def verify_python_dependencies():
    """Check if required Python packages are available"""
    required_packages = [
        'psycopg2-binary',
        'redis',
        'qdrant-client',
        'fastapi',
        'uvicorn',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"[AVISO] Pacotes faltando: {', '.join(missing)}")
        print("       Execute: pip install -r requirements-dev.txt")
        return False
    else:
        print("[OK] Todas as dependencias Python instaladas")
        return True


def main():
    print("\n" + "="*70)
    print("SETUP - ESTEIRA DE DESENVOLVIMENTO LEXGRID")
    print("="*70 + "\n")
    
    print("[*] Criando estrutura de scripts...")
    if not create_scripts_directory():
        return 1
    
    print("\n[*] Configurando Git hooks...")
    if not setup_git_hooks():
        return 1
    
    print("\n[*] Verificando Docker...")
    docker_ok = verify_docker_containers()
    
    print("\n[*] Verificando dependencias Python...")
    python_ok = verify_python_dependencies()
    
    print("\n" + "="*70)
    print("RESUMO DO SETUP")
    print("="*70)
    print(f"Git Hooks:              [OK]")
    print(f"Docker:                 {'[OK]' if docker_ok else '[AVISO]'}")
    print(f"Dependencias Python:    {'[OK]' if python_ok else '[AVISO]'}")
    print("="*70)
    
    if docker_ok and python_ok:
        print("\n[SUCESSO] Esteira completamente configurada!")
        print("\nProximos passos:")
        print("  1. Adicione arquivos: git add .")
        print("  2. Faça commit: git commit -m 'setup: esteira de desenvolvimento'")
        print("  3. O hook executara automaticamente!")
        return 0
    else:
        print("\n[AVISO] Setup parcialmente completo.")
        print("        Corrija os problemas listados acima.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[CANCELADO] Setup interrompido")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] Falha no setup: {e}")
        sys.exit(1)
