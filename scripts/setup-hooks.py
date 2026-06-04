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
    
    print("[*] Instalando hooks via biblioteca pre-commit...")
    try:
        subprocess.run(
            "pre-commit install",
            shell=True,
            cwd=project_root,
            check=True
        )
        print(f"[OK] Git hooks instalados com sucesso via pre-commit")
    except Exception as e:
        print(f"[AVISO] Falha ao configurar git hooks: {e}")
        print("        Verifique se o pacote 'pre-commit' esta instalado (pip install pre-commit).")
        return False
    
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
