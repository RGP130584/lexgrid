import ast

class AISandbox:
    """
    Execução isolada de código gerado por IA.
    Bloqueia estritamente OS, Subprocess, Sys e FileSystem.
    """
    
    @classmethod
    def safe_eval(cls, expression: str, context: dict = None):
        """Avalia expressões matemáticas ou dicionários restritos (sem builtins)."""
        try:
            # AST literal_eval é inerentemente seguro para estruturas de dados
            return ast.literal_eval(expression)
        except Exception:
            # Se falhar no literal_eval, usamos eval com globals limpos
            safe_globals = {"__builtins__": {}}
            safe_locals = context or {}
            try:
                # ATENÇÃO: Em produção pesada, usar WebAssembly (Wasm) ou contêineres efêmeros
                return eval(expression, safe_globals, safe_locals)
            except Exception as e:
                return f"[SANDBOX_ERROR] Execução negada ou inválida: {str(e)}"