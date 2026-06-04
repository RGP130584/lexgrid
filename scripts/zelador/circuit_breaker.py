from datetime import datetime
from .config import CircuitBreakerConfig

class CircuitBreaker:
    def __init__(self):
        self.failures = {}
        self.last_failure_time = {}

    def record_failure(self, service_name: str):
        self.failures[service_name] = self.failures.get(service_name, 0) + 1
        self.last_failure_time[service_name] = datetime.now()

    def is_open(self, service_name: str) -> bool:
        if self.failures.get(service_name, 0) >= CircuitBreakerConfig.FAILURE_THRESHOLD:
            time_since_failure = (datetime.now() - self.last_failure_time[service_name]).total_seconds()
            if time_since_failure < CircuitBreakerConfig.COOLDOWN_PERIOD:
                return True
        return False

    def reset(self, service_name: str):
        self.failures[service_name] = 0
        self.last_failure_time.pop(service_name, None)