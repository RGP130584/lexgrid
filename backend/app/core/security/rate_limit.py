from fastapi import Request, HTTPException
import time

_rate_limit_store = {}

def check_rate_limit(request: Request, limit: int = 10, window: int = 60):
    """Validação básica de Rate Limit e anti-abuso."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    if client_ip not in _rate_limit_store:
        _rate_limit_store[client_ip] = []
        
    requests = [req_time for req_time in _rate_limit_store[client_ip] if now - req_time < window]
    
    if len(requests) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit excedido.")
        
    requests.append(now)
    _rate_limit_store[client_ip] = requests