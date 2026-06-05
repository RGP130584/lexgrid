import jwt
from datetime import datetime, timedelta, timezone
import os

JWT_SECRET = os.getenv("JWT_SECRET", "sua-chave-secreta-aqui")
ALGORITHM = "HS256"

def create_access_token(key_used: str, expires_delta: timedelta = timedelta(hours=2)) -> str:
    """Gera um token JWT para o Beta Tester expitando em 2 horas."""
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "role": "beta_tester",
        "key_used": key_used
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decodifica e valida o token JWT. Retorna o payload se valido, senao None."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
