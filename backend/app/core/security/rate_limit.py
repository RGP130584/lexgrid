from fastapi import Request, HTTPException
import time

_rate_limit_store = {}
_ai_rate_limit_store = {}

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


def check_ai_rate_limit(request: Request):
    """
    Escudo Anti-Spam: Limita a 15 chamadas na IA a cada 15 minutos por usuário.
    """
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = 15 * 60  # 15 minutos em segundos
    limit = 15
    
    if client_ip not in _ai_rate_limit_store:
        _ai_rate_limit_store[client_ip] = []
        
    requests = [req_time for req_time in _ai_rate_limit_store[client_ip] if now - req_time < window]
    
    if len(requests) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Para garantir a estabilidade do sistema em fase Beta, limite de análises atingido. Por favor, aguarde alguns minutos para gerar novos relatórios."
        )
        
    requests.append(now)
    _ai_rate_limit_store[client_ip] = requests


def beta_access_bypass(request: Request):
    """
    Middleware/Dependência que libera acesso global para a Fase Beta
    (Substitui futuras checagens de pagamento).
    """
    # TODO Futuro: Aqui entrará a lógica de planos e assinaturas.
    # Por enquanto, todos os usuários logados com a Chave Beta têm passe livre.
    request.state.is_premium = True