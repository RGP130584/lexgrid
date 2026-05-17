import pytest
from scripts.zelador.circuit_breaker import CircuitBreaker
from scripts.zelador.port_manager import PortManager
from scripts.zelador.config import CircuitBreakerConfig

def test_circuit_breaker():
    cb = CircuitBreaker()
    service = "test_service"
    
    assert not cb.is_open(service)
    for _ in range(CircuitBreakerConfig.FAILURE_THRESHOLD):
        cb.record_failure(service)
    
    assert cb.is_open(service)
    cb.reset(service)
    assert not cb.is_open(service)

def test_port_manager_offline():
    # Assumindo que a porta 99999 não existe e vai dar erro ou timeout
    assert not PortManager.is_port_open(59999)