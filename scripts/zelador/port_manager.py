import socket

class PortManager:
    @staticmethod
    def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((host, port)) == 0

    @staticmethod
    def check_conflicts(ports: list) -> dict:
        conflicts = {p: PortManager.is_port_open(p) for p in ports}
        return conflicts