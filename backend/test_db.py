#!/usr/bin/env python3
"""
LexGrid Database Tests
Validates database connections before commits
"""

import psycopg2
import redis
from qdrant_client import QdrantClient
import time
import sys


def test_postgres():
    """Test PostgreSQL connection"""
    try:
        conn = psycopg2.connect(
            dbname="lexgrid_core",
            user="lexadmin",
            password="lexpassword_secure_2026",
            host="localhost",
            port="5432"
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
        print(f"[ERRO] PostgreSQL falhou: {str(e)[:100]}")
        return False


def test_redis():
    """Test Dragonfly (Redis compatible)"""
    try:
        r = redis.Redis(
            host='localhost',
            port=6379,
            password='dragonfly_secure_pass',
            decode_responses=True
        )
        r.ping()
        info = r.info('server')
        print("[OK] Dragonfly (Redis) conectado com sucesso")
        print(f"     Versao: {info.get('redis_version', 'N/A')}")
        return True
    except Exception as e:
        print(f"[ERRO] Dragonfly falhou: {str(e)[:100]}")
        return False


def test_qdrant():
    """Test Qdrant Vector Database"""
    try:
        qdrant = QdrantClient(host="localhost", port=6333)
        collections = qdrant.get_collections()
        print("[OK] Qdrant conectado com sucesso")
        print(f"     Colecoes: {len(collections.collections)}")
        return True
    except Exception as e:
        print(f"[ERRO] Qdrant falhou: {str(e)[:100]}")
        return False


def test_ollama():
    """Test Ollama LLM Service"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("[OK] Ollama conectado com sucesso")
            print(f"     Modelos: {len(models)} disponivel(is)")
            return True
        else:
            print(f"[ERRO] Ollama retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERRO] Ollama falhou: {str(e)[:100]}")
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
        failed = [k for k, v in results.items() if not v]
        print(f"[AVISO] Servicos com problemas: {', '.join(failed)}")
        print("\nAtenção: Alguns servicos nao responderam.")
        print("Verifique se os containers Docker estao rodando:")
        print("  docker compose -f backend/docker-compose.yml up -d")
        return 1


if __name__ == "__main__":
    sys.exit(main())
