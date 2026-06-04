SERVICES_CONFIG = {
    "postgres": {"container": "lexgrid_postgres", "port": 55433},
    "dragonfly": {"container": "lexgrid_dragonfly", "port": 56379},
    "qdrant": {"container": "lexgrid_qdrant", "port": 56333},
    "ollama": {"container": "lexgrid_ollama", "port": 51434},
    "vault": {"container": "lexgrid_vault", "port": 8200}
}

COMPOSE_FILE_PATH = "docker-compose.yml"
NETWORK_NAME = "lexgrid_secure_net"
VOLUMES = ["postgres_data", "qdrant_data", "ollama_data"]