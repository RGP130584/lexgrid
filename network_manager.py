import subprocess

class NetworkManager:
    def __init__(self, logger):
        self.logger = logger

    def prune_networks(self):
        self.logger.info("Limpando redes Docker órfãs (Network Prune)...")
        res = subprocess.run(["docker", "network", "prune", "-f"], capture_output=True, text=True)
        return res.returncode == 0