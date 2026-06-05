from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
import random
from infrastructure.database.db_connection import get_db_connection
from app.core.security.jwt import create_access_token
import psycopg2

router = APIRouter()

class BetaLoginRequest(BaseModel):
    key_hash: str = Field(..., min_length=6, max_length=6)

def generate_beta_key() -> str:
    # Excluidos: O, 0, I, l, 1 para evitar ambiguidade visual
    chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    return ''.join(random.choice(chars) for _ in range(6))

@router.post("/admin-control/generate-key")
async def generate_key():
    # TODO: Inserir middleware de autenticacao Master/Admin aqui
    new_key = generate_beta_key()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO access_keys (key_hash, max_uses, current_uses, is_active) 
                    VALUES (%s, 5, 0, True)
                    """,
                    (new_key,)
                )
            conn.commit()
        return {"success": True, "key": new_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar chave no banco: {e}")

@router.post("/login/beta")
async def login_beta(payload: BetaLoginRequest):
    key_hash = payload.key_hash.strip().upper()
    
    conn = get_db_connection()
    try:
        # Iniciamos a transação explicitamente para garantir Atomicidade e lock FOR UPDATE
        with conn:
            with conn.cursor() as cur:
                # Busca a chave travando a linha para atualizacao (FOR UPDATE)
                cur.execute(
                    """
                    SELECT id, key_hash, max_uses, current_uses, is_active 
                    FROM access_keys 
                    WHERE key_hash = %s 
                    FOR UPDATE
                    """,
                    (key_hash,)
                )
                res = cur.fetchone()
                
                if not res:
                    raise HTTPException(status_code=401, detail="Chave nao encontrada.")
                    
                key_id, kh, max_uses, current_uses, is_active = res
                
                # Validacoes
                if not is_active:
                    raise HTTPException(status_code=401, detail="Esta chave foi desativada.")
                    
                if current_uses >= max_uses:
                    raise HTTPException(status_code=401, detail="Esta chave atingiu o limite maximo de testes.")
                    
                # Incrementa o uso
                new_uses = current_uses + 1
                will_be_active = new_uses < max_uses
                
                # Atualiza a chave no banco
                cur.execute(
                    """
                    UPDATE access_keys 
                    SET current_uses = %s, is_active = %s 
                    WHERE id = %s
                    """,
                    (new_uses, will_be_active, key_id)
                )
        # O commit é executado automaticamente ao sair com sucesso do bloco 'with conn'
        
        # Gera o Token da sessao (Expira em 2 horas)
        token = create_access_token(key_used=key_hash)
        
        return {
            "success": True,
            "token": token,
            "uses_left": max_uses - new_uses
        }
        
    except HTTPException:
        # Rollback automático pelo cursor/conn context manager
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")
    finally:
        conn.close()

@router.get("/admin-control/keys")
async def list_keys():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, key_hash, max_uses, current_uses, is_active, created_at 
                    FROM access_keys 
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()
                keys = []
                for r in rows:
                    keys.append({
                        "id": r[0],
                        "key_hash": r[1],
                        "max_uses": r[2],
                        "current_uses": r[3],
                        "is_active": r[4],
                        "created_at": r[5].isoformat() if r[5] else None
                    })
        return keys
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar chaves: {e}")

@router.post("/admin-control/keys/{key_id}/toggle")
async def toggle_key(key_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE access_keys SET is_active = NOT is_active WHERE id = %s RETURNING is_active", (key_id,))
                res = cur.fetchone()
                if not res:
                    raise HTTPException(status_code=404, detail="Chave nao encontrada.")
                new_state = res[0]
            conn.commit()
        return {"success": True, "is_active": new_state}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao alternar status da chave: {e}")

class UpdateMaxUsesRequest(BaseModel):
    max_uses: int = Field(..., ge=1)

@router.post("/admin-control/keys/{key_id}/max-uses")
async def update_max_uses(key_id: int, payload: UpdateMaxUsesRequest):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_uses FROM access_keys WHERE id = %s", (key_id,))
                res = cur.fetchone()
                if not res:
                    raise HTTPException(status_code=404, detail="Chave nao encontrada.")
                current_uses = res[0]
                
                is_active = current_uses < payload.max_uses
                
                cur.execute(
                    """
                    UPDATE access_keys 
                    SET max_uses = %s, is_active = %s 
                    WHERE id = %s 
                    RETURNING max_uses, is_active
                    """,
                    (payload.max_uses, is_active, key_id)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Chave nao encontrada.")
                updated_max_uses, updated_is_active = row
            conn.commit()
        return {
            "success": True, 
            "max_uses": updated_max_uses, 
            "is_active": updated_is_active
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar limite de usos: {e}")

@router.delete("/admin-control/keys/{key_id}")
async def delete_key(key_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM access_keys WHERE id = %s RETURNING id", (key_id,))
                res = cur.fetchone()
                if not res:
                    raise HTTPException(status_code=404, detail="Chave nao encontrada.")
            conn.commit()
        return {"success": True, "message": "Chave deletada com sucesso."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar chave: {e}")


