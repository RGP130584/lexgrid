import yaml
from pathlib import Path

class DockerHardeningValidator:
    """Garante via Policy-as-Code que os containers rodam isolados e restritos."""
    
    REQUIRED_POLICIES = ["no-new-privileges:true"]
    
    @classmethod
    def validate_compose(cls, compose_path: Path) -> list:
        violations = []
        with open(compose_path, 'r') as f:
            data = yaml.safe_load(f)
            
        for service_name, config in data.get('services', {}).items():
            # Verifica read_only_root_filesystem
            if not config.get('read_only', False):
                violations.append(f"Serviço {service_name} carece de read_only root filesystem.")
                
            # Verifica drop capabilities
            caps = config.get('cap_drop', [])
            if "ALL" not in caps and "all" not in caps:
                violations.append(f"Serviço {service_name} não aplica cap_drop: ALL.")
                
            # Verifica no-new-privileges
            sec_opts = config.get('security_opt', [])
            if not any(req in opt for req in cls.REQUIRED_POLICIES for opt in sec_opts):
                violations.append(f"Serviço {service_name} carece de no-new-privileges.")
                
        return violations