import subprocess
import re
import psycopg2
import sys
import urllib.request
import urllib.error

def get_docker_host():
    try:
        out = subprocess.check_output(["wsl", "ip", "addr", "show", "eth0"], text=True)
        match = re.search(r"inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", out)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "localhost"

host = get_docker_host()

print(f"Connecting to Postgres host: {host}:55433")

try:
    # Conecta ao Postgres mapeado na porta 55433
    conn = psycopg2.connect(
        dbname='lexgrid_core', 
        user='lexadmin', 
        password='lexpassword_secure_2026', 
        host=host, 
        port='55433',
        connect_timeout=3
    )
    conn.close()
    print("Postgres: SUCCESS")
except Exception as e:
    print("Postgres REPR:", repr(e))

print(f"Connecting to Qdrant host: http://{host}:56333")
try:
    # Consulta a rota de readiness do Qdrant usando a porta HTTP (56333)
    qdrant_url = f"http://{host}:56333/readyz"
    req = urllib.request.Request(qdrant_url)
    with urllib.request.urlopen(req, timeout=3) as response:
        if response.status == 200:
            print("Qdrant: SUCCESS")
        else:
            print(f"Qdrant: FAILED (Status {response.status})")
except Exception as e:
    print("Qdrant REPR:", repr(e))