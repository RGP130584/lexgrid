import subprocess
from pathlib import Path
from .constants import COMPOSE_FILE_PATH
from .config import PROJECT_ROOT

class DockerManager:
    def __init__(self, logger):
        self.logger = logger
        self.compose_file = PROJECT_ROOT / COMPOSE_FILE_PATH

    def _run(self, cmd: list) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)

    def is_engine_running(self) -> bool:
        res = self._run(["docker", "info"])
        return res.returncode == 0

    def compose_up(self, force_recreate=False):
        cmd = ["docker", "compose", "-f", str(self.compose_file), "up", "-d"]
        if force_recreate:
            cmd.append("--force-recreate")
        self.logger.info(f"Executando Compose UP... Forçado={force_recreate}")
        return self._run(cmd).returncode == 0

    def compose_down(self, remove_volumes=False):
        cmd = ["docker", "compose", "-f", str(self.compose_file), "down"]
        if remove_volumes:
            cmd.append("-v")
        self.logger.info(f"Executando Compose DOWN... Wipe={remove_volumes}")
        return self._run(cmd).returncode == 0

    def get_container_status(self, container_name: str) -> str:
        res = self._run(["docker", "inspect", "--format={{.State.Health.Status}}", container_name])
        if res.returncode != 0:
            res = self._run(["docker", "inspect", "--format={{.State.Status}}", container_name])
            if res.returncode != 0:
                return "missing"
        return res.stdout.strip()