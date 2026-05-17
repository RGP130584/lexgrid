import json
from scripts.shared.logger import get_logger # Utiliza framework base
from observability.logging.correlation import set_correlation_id, get_correlation_id
from observability.logging.sanitizer import LogSanitizer

def test_correlation_id_lifecycle():
    cid1 = set_correlation_id()
    assert get_correlation_id() == cid1
    
    cid2 = set_correlation_id("custom-trace-999")
    assert get_correlation_id() == "custom-trace-999"
    assert cid1 != cid2

def test_log_sanitizer_dict():
    raw_data = {
        "user": "admin",
        "password": "supersecretpassword",
        "api_key": "AKIAIOSFODNN7EXAMPLE",
        "safe_data": "ok"
    }
    sanitized = LogSanitizer.sanitize_dict(raw_data)
    assert sanitized["user"] == "admin"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["api_key"] == "[REDACTED]"