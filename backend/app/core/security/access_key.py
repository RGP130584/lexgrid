from fastapi import Request, HTTPException, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from infrastructure.database.db_connection import get_db_connection
import psycopg2

X_ACCESS_KEY_HEADER = APIKeyHeader(name="X-Access-Key", auto_error=False)
ACCESS_KEY_QUERY = APIKeyQuery(name="key", auto_error=False)

def verify_access_key(
    header_key: str = Security(X_ACCESS_KEY_HEADER),
    query_key: str = Security(ACCESS_KEY_QUERY)
) -> str:
    """
    Valida a chave de acesso (via Header X-Access-Key ou Query Param ?key).
    Retorna a chave se for valida e incrementa o contador de uso.
    """
    key = header_key or query_key
    if not key:
        raise HTTPException(
            status_code=401,
            detail="Chave de acesso (Access Key) e obrigatoria. Use o cabecalho X-Access-Key ou o parametro ?key."
        )
        
    if len(key) != 6:
        raise HTTPException(
            status_code=403,
            detail="Chave de acesso invalida (deve conter exatamente 6 caracteres)."
        )

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Busca a chave ativa e com saldo de usos
                cur.execute(
                    """
                    SELECT is_active, current_uses, max_uses 
                    FROM access_keys 
                    WHERE key_hash = %s
                    """,
                    (key,)
                )
                res = cur.fetchone()
                
                if not res:
                    raise HTTPException(
                        status_code=403,
                        detail="Chave de acesso nao encontrada ou invalida."
                    )
                    
                is_active, current_uses, max_uses = res
                
                if not is_active:
                    raise HTTPException(
                        status_code=403,
                        detail="Chave de acesso inativa."
                    )
                    
                if current_uses >= max_uses:
                    raise HTTPException(
                        status_code=403,
                        detail="Limite de consultas desta chave de acesso atingido."
                    )
                    
                # Incrementa o contador de usos e desativa se atingir o limite
                new_uses = current_uses + 1
                should_deactivate = new_uses >= max_uses
                
                cur.execute(
                    """
                    UPDATE access_keys 
                    SET current_uses = %s, is_active = %s 
                    WHERE key_hash = %s
                    """,
                    (new_uses, not should_deactivate, key)
                )
            conn.commit()
            
        return key
    except HTTPException:
        raise
    except Exception as e:
        # Fallback de seguranca caso o banco de dados falhe
        print(f"[ACCESS KEY] Erro ao validar chave de acesso no banco: {e}")
        # Chaves mockadas em memoria caso o banco esteja indisponivel
        MOCK_KEYS = {"LXG123": 5, "ADM001": 100, "DEV777": 10}
        if key in MOCK_KEYS:
            return key
        raise HTTPException(
            status_code=500,
            detail="Erro de infraestrutura ao validar a chave de acesso."
        )
