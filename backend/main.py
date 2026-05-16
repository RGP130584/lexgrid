from fastapi import FastAPI
from qdrant_client import QdrantClient
import redis
import psycopg2

app = FastAPI(
    title="LexGrid Core API",
    description="Espinha dorsal cognitiva para inteligência fiscal e jurídica",
    version="2.0.0"
)

@app.get("/")
def read_root():
    return {"status": "online", "system": "LexGrid"}

@app.get("/health/storage")
def check_health():
    health_status = {}
    
    # 1. Testar Conexão com a Memória Curta (Dragonfly)
    try:
        r = redis.Redis(host='localhost', port=6379, password='dragonfly_secure_pass', decode_responses=True)
        r.ping()
        health_status["dragonfly_cache"] = "⚡ Conectado"
    except Exception as e:
        health_status["dragonfly_cache"] = f"❌ Erro: {str(e)}"

    # 2. Testar Conexão com a Memória Semântica (Qdrant Vetorial)
    try:
        qdrant = QdrantClient(host="localhost", port=6333)
        qdrant.get_collections()
        health_status["qdrant_vector"] = "🧠 Conectado"
    except Exception as e:
        health_status["qdrant_vector"] = f"❌ Erro: {str(e)}"

    # 3. Testar Conexão com a Memória Longa (PostgreSQL)
    try:
        conn = psycopg2.connect(
            dbname="lexgrid_core",
            user="lexadmin",
            password="lexpassword_secure_2026",
            host="localhost",
            port="5432"
        )
        conn.close()
        health_status["postgres_relational"] = "💾 Conectado"
    except Exception as e:
        health_status["postgres_relational"] = f"❌ Erro: {str(e)}"

    return health_status
