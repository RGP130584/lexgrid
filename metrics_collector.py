from prometheus_client import Counter, Histogram, Gauge

class LexGridMetrics:
    """Registro Central de Métricas da Aplicação."""
    
    # --- Infraestrutura ---
    ACTIVE_CONNECTIONS = Gauge('lexgrid_active_connections', 'Conexões ativas no banco de dados')
    
    # --- Inteligência Artificial ---
    LLM_REQUESTS = Counter('lexgrid_llm_requests_total', 'Total de requisições de IA', ['model', 'status'])
    LLM_TOKENS = Counter('lexgrid_llm_tokens_total', 'Total de tokens consumidos', ['model'])
    LLM_LATENCY = Histogram('lexgrid_llm_latency_seconds', 'Latência das requisições IA', ['model'])
    
    # --- Segurança e Governança ---
    SECURITY_BLOCKS = Counter('lexgrid_security_blocks_total', 'Total de interações bloqueadas', ['reason'])
    JAILBREAK_ATTEMPTS = Counter('lexgrid_jailbreak_attempts_total', 'Tentativas de Jailbreak detectadas')
    
    @classmethod
    def record_ai_request(cls, model: str, status: str, tokens: int, latency: float):
        cls.LLM_REQUESTS.labels(model=model, status=status).inc()
        cls.LLM_TOKENS.labels(model=model).inc(tokens)
        cls.LLM_LATENCY.labels(model=model).observe(latency)

    @classmethod
    def record_security_block(cls, reason: str):
        cls.SECURITY_BLOCKS.labels(reason=reason).inc()