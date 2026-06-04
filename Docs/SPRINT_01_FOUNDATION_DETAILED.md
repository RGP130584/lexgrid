# SPRINT_01_FOUNDATION_DETAILED.md

# Sprint 01 — Foundation Detailed
Versão 1.0

## Objetivo

Criar a fundação operacional do LexGrid para que todas as demais sprints possam ser executadas sobre uma base estável, reproduzível e auditável.

---

# Resultado Esperado

Ao final desta sprint deverá existir:

- FastAPI operacional
- PostgreSQL operacional
- Qdrant operacional
- Dragonfly operacional
- Ollama operacional
- Docker Compose funcional
- Healthchecks funcionais
- Observabilidade básica
- Estrutura de diretórios oficial
- Pipeline de testes inicial

---

# Arquitetura Alvo

Usuário
↓
FastAPI
↓
Services
↓
PostgreSQL
Qdrant
Dragonfly
Ollama

---

# Estrutura de Diretórios

lexgrid/

app/
api/
modules/
services/
engines/
repositories/
models/
core/
utils/

tests/
scripts/
docs/
knowledge/
data/
infrastructure/

---

# Arquivos Obrigatórios

app/main.py

Responsabilidades:
- Inicialização FastAPI
- Registro de rotas
- Startup
- Shutdown
- Middleware

---

app/core/config.py

Responsabilidades:
- Configuração central
- Variáveis de ambiente
- Feature flags

---

app/core/logging.py

Responsabilidades:
- Logging estruturado
- Integração futura com observabilidade

---

app/api/routers/health.py

Endpoints:

GET /health
GET /health/database
GET /health/qdrant
GET /health/cache
GET /health/ollama

---

# Docker Compose

Serviços:

backend
postgres
qdrant
dragonfly
ollama
prometheus
grafana

Todos com:

- restart policy
- healthcheck
- volumes
- networks

---

# Variáveis de Ambiente

Criar:

.env.example

Campos mínimos:

APP_ENV
API_HOST
API_PORT

POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD

QDRANT_HOST
QDRANT_PORT

DRAGONFLY_HOST
DRAGONFLY_PORT

OLLAMA_HOST

JWT_SECRET_KEY

LOG_LEVEL

---

# Banco de Dados

PostgreSQL

Objetivo inicial:

- auditoria
- metadados
- configurações

Não criar tabelas de negócio ainda.

---

# Qdrant

Criar collections vazias:

- tax
- legal
- incentives
- agro
- energy

---

# Dragonfly

Objetivo:

- cache de consultas
- cache de enrichment
- cache de retrieval

---

# Ollama

Modelo inicial:

- llama3

Objetivo:

- testes locais
- integração futura

---

# Observabilidade

Prometheus

Coletar:

- uptime
- requests
- latência

Grafana

Dashboard inicial:

- API
- banco
- cache

---

# Testes Obrigatórios

tests/

test_health.py
test_database.py
test_qdrant.py
test_cache.py
test_ollama.py

---

# Critérios de Aceite

docker compose up -d

Todos os containers saudáveis.

GET /health retorna 200.

GET /health/database retorna 200.

GET /health/qdrant retorna 200.

GET /health/cache retorna 200.

GET /health/ollama retorna 200.

---

# Definition of Done

[ ] Estrutura criada
[ ] Docker funcional
[ ] FastAPI funcional
[ ] PostgreSQL funcional
[ ] Qdrant funcional
[ ] Dragonfly funcional
[ ] Ollama funcional
[ ] Testes criados
[ ] README atualizado
[ ] Healthchecks funcionais

---

# Anti-Padrões

Não colocar lógica de negócio nesta sprint.

Não implementar agentes.

Não implementar RAG.

Não implementar Opportunity Engine.

Não implementar Judge.

Objetivo exclusivo:
Fundação técnica do projeto.

---

# Próxima Sprint

SPRINT_02_CNPJ_INTELLIGENCE_DETAILED.md
