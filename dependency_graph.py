class DependencyGraph:
    """Mapeia a árvore de dependência de inicialização para startup ordenado."""
    def __init__(self):
        self.graph = {
            "docker_engine": [],
            "vault": ["docker_engine"],
            "postgres": ["vault", "docker_engine"],
            "dragonfly": ["docker_engine"],
            "qdrant": ["docker_engine"],
            "ollama": ["docker_engine"]
        }
    def get_startup_order(self):
        return ["docker_engine", "vault", "postgres", "dragonfly", "qdrant", "ollama"]