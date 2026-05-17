import subprocess

class VolumeManager:
    def __init__(self, logger):
        self.logger = logger

    def purge_volumes(self, volumes: list):
        self.logger.warning("Purgando volumes (Tática Extrema)...")
        for vol in volumes:
            subprocess.run(["docker", "volume", "rm", "-f", f"lexgrid_{vol}"], capture_output=True)