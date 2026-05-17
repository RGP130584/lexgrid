import uuid
import contextvars

# Armazenamento de contexto isolado por thread/async task
_correlation_id = contextvars.ContextVar("correlation_id", default=None)

def set_correlation_id(cid: str = None) -> str:
    """Define ou gera um novo Correlation ID para a request atual."""
    if not cid:
        cid = str(uuid.uuid4())
    _correlation_id.set(cid)
    return cid

def get_correlation_id() -> str:
    """Recupera o Correlation ID atual."""
    cid = _correlation_id.get()
    if not cid:
        return set_correlation_id()
    return cid