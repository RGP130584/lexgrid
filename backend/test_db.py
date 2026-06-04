#!/usr/bin/env python3
"""
LexGrid Database Tests
Validates database connections before commits
"""

import psycopg2
import redis
from qdrant_client import QdrantClient
import time
import os
import sys


def test_postgres():
    """Test PostgreSQL connection"""
    try:
        conn = psycopg2.connect(
            dbname="lexgrid_core",
            user=os.getenv("POSTGRES_USER", "lexadmin"),
            password=os.getenv("POSTGRES_PASSWORD", "lexpassword_secure_2026"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "55433")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        print("[OK] PostgreSQL conectado com sucesso")
        print(f"     Versao: {version[0][:50]}...")
        return True
    except Exception as e:
        print(f"[ERRO] PostgreSQL falhou: {repr(e)[:100]}")
        return False


def test_redis():
    """Test Dragonfly (Redis compatible)"""
    try:
        r = redis.Redis(
            host='localhost',
            port=int(os.getenv("DRAGONFLY_PORT", 56379)),
            password=os.getenv("DRAGONFLY_PASSWORD", "dragonfly_secure_pass"),
            decode_responses=True
        )
        r.ping()
        info = r.info('server')
        print("[OK] Dragonfly (Redis) conectado com sucesso")
        print(f"     Versao: {info.get('redis_version', 'N/A')}")
        return True
    except Exception as e:
        print(f"[ERRO] Dragonfly falhou: {repr(e)[:100]}")
        return False


def test_qdrant():
    """Test Qdrant Vector Database"""
    try:
        qdrant = QdrantClient(host="localhost", port=int(os.getenv("QDRANT_PORT", 56333)), check_compatibility=False)
        collections = qdrant.get_collections()
        print("[OK] Qdrant conectado com sucesso")
        print(f"     Colecoes: {len(collections.collections)}")
        return True
    except Exception as e:
        print(f"[ERRO] Qdrant falhou: {repr(e)[:100]}")
        return False


def test_ollama():
    """Test Ollama LLM Service"""
    try:
        import requests
        port = os.getenv("OLLAMA_PORT", 51434)
        response = requests.get(f'http://localhost:{port}/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("[OK] Ollama conectado com sucesso")
            print(f"     Modelos: {len(models)} disponivel(is)")
            return True
        else:
            print(f"[ERRO] Ollama retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERRO] Ollama falhou: {repr(e)[:100]}")
        return False


def attempt_recovery():
    """Delega a recuperação profunda e proativa para o Agente Zelador."""
    print("\n[*] Detectada falha na infraestrutura. Acionando Agente Zelador para auto-reparo...")
    try:
        import subprocess
        base_path = os.path.dirname(os.path.abspath(__file__))
        zelador_script = os.path.join(base_path, "..", "scripts", "zelador.py")
        
        subprocess.Popen([sys.executable, zelador_script, "--repair"])
        return False # Delega assincronamente. O CI/CD irá checar via wait_for_services
    except Exception as e:
        print(f"[ERRO] Falha crítica ao acionar o Zelador: {repr(e)}")
        return False


def main():
    print("\n" + "="*60)
    print("VALIDACAO DE BANCO DE DADOS - PRE-COMMIT")
    print("="*60 + "\n")
    
    results = {
        "PostgreSQL": test_postgres(),
        "Dragonfly": test_redis(),
        "Qdrant": test_qdrant(),
        "Ollama": test_ollama()
    }
    
    print("\n" + "="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"RESULTADO: {passed}/{total} servicos funcionais")
    print("="*60 + "\n")
    
    if passed == total:
        print("[SUCESSO] Todos os servicos estao saudaveis!")
        return 0
    else:
        # Se houver falha, tenta recuperar automaticamente antes de desistir
        if attempt_recovery():
            print("[*] [ZELADOR] Re-executando testes de integridade...")
            results_retry = {
                "PostgreSQL": test_postgres(),
                "Dragonfly": test_redis(),
                "Qdrant": test_qdrant(),
                "Ollama": test_ollama()
            }
            if all(results_retry.values()):
                print("\n" + "="*60)
                print("[SUCESSO] Recuperação automática concluída com êxito!")
                print("="*60 + "\n")
                return 0

        failed = [k for k, v in results.items() if not v]
        print(f"[AVISO] Servicos com problemas: {', '.join(failed)}")
        print("\nAtenção: Alguns servicos nao responderam.")
        print("Verifique se os containers Docker estao rodando:")
        print("  docker compose -f backend/docker-compose.yml up -d")
        return 1


if __name__ == "__main__":
    sys.exit(main())
