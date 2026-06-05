from infrastructure.database.db_connection import get_db_connection

def init_database():
    """Garante a criacao das tabelas sped_files e access_keys e insere chaves default de teste."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # 1. Tabela de arquivos SPED
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sped_files (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255),
                        file_type VARCHAR(100),
                        records_count INT,
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 2. Tabela de Chaves de Acesso
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS access_keys (
                        id SERIAL PRIMARY KEY,
                        key_hash VARCHAR(6) UNIQUE NOT NULL,
                        max_uses INT DEFAULT 5,
                        current_uses INT DEFAULT 0,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 3. Carga Inicial de Chaves para desenvolvimento/teste
                default_keys = [
                    ("LXG123", 5),
                    ("ADM001", 100),
                    ("DEV777", 10)
                ]
                for key, max_uses in default_keys:
                    cur.execute("""
                        INSERT INTO access_keys (key_hash, max_uses)
                        VALUES (%s, %s)
                        ON CONFLICT (key_hash) DO NOTHING;
                    """, (key, max_uses))
                    
            conn.commit()
            print("[DATABASE] Inicializacao concluida com sucesso.")
    except Exception as e:
        print(f"[DATABASE] Falha critica na inicializacao: {e}")
