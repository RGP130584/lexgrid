# SPRINT_02_CNPJ_INTELLIGENCE_DETAILED.md

# Sprint 02 — CNPJ Intelligence Detailed
Versão 1.0

## Objetivo

Transformar um CNPJ em um perfil empresarial estruturado e enriquecido que será utilizado por todos os motores do LexGrid.

Esta sprint é a porta de entrada do sistema.

Sem ela não existe:

- Opportunity Engine
- Rules Engine
- Scoring Engine
- Judge Engine
- Executive Reports

---

# Resultado Esperado

Entrada:

{
  "cnpj": "00000000000191"
}

Saída:

{
  "company_profile": {
    "legal_name": "",
    "trade_name": "",
    "cnaes": [],
    "segment": "",
    "state": "",
    "city": "",
    "size": ""
  }
}

---

# Arquitetura

Usuário
↓
API
↓
CNPJ Validator
↓
Receita Connector
↓
Enrichment Engine
↓
Company Profile
↓
PostgreSQL + Cache

---

# Estrutura de Diretórios

app/modules/cnpj/

Arquivos:

validator.py
connector.py
enrichment.py
classifier.py
models.py
service.py

---

# TASK-0201
## CNPJ Validator

Responsabilidades:

- remover caracteres inválidos
- validar tamanho
- validar dígitos verificadores
- normalizar formato

Regras:

- aceitar com máscara
- aceitar sem máscara
- rejeitar CNPJ inválido

---

# TASK-0202
## Receita Connector

Objetivo:

Consultar fontes oficiais e autorizadas para obter:

- Razão Social
- Nome Fantasia
- CNAEs
- Situação Cadastral
- Endereço
- Município
- Estado
- Data de abertura

Requisitos:

- timeout
- retry
- cache
- logs

---

# TASK-0203
## CNAE Mapping

Objetivo:

Transformar CNAEs em segmentos de negócio.

Categorias iniciais:

- Agro
- Energia
- Indústria
- Comércio
- Tecnologia
- Saúde
- Educação
- Logística

---

# TASK-0204
## Company Classifier

Objetivo:

Classificar automaticamente a empresa.

Entradas:

- CNAE Principal
- CNAEs Secundários
- Porte
- Localização

Saídas:

- segmento
- subsetor
- perfil tributário inicial

---

# TASK-0205
## Enrichment Engine

Objetivo:

Construir CompanyProfile.

Campos obrigatórios:

company_id
cnpj
legal_name
trade_name
state
city
size
cnaes
segment
subsegment

---

# Endpoint

POST /api/v1/cnpj/analyze

Request:

{
  "cnpj": "00000000000191"
}

Response:

{
  "success": true,
  "company_profile": {}
}

---

# PostgreSQL

Tabela:

company_profiles

Campos:

id
cnpj
legal_name
trade_name
segment
subsegment
state
city
created_at
updated_at

---

# Dragonfly Cache

Chave:

cnpj:{cnpj}

TTL:

24 horas

---

# Observabilidade

Métricas:

- consultas realizadas
- tempo médio
- falhas
- cache hits

---

# Testes

test_cnpj_validator.py
test_connector.py
test_classifier.py
test_enrichment.py

---

# Critérios de Aceite

✓ CNPJ válido processado

✓ Perfil empresarial gerado

✓ Endpoint funcional

✓ Cache funcional

✓ Logs funcionais

✓ Testes passando

---

# Definition of Done

[ ] Validator implementado
[ ] Connector implementado
[ ] Classifier implementado
[ ] Enrichment implementado
[ ] Endpoint criado
[ ] Testes criados
[ ] Documentação atualizada

---

# Anti-Padrões

Não usar LLM para classificar CNAE.

Não usar scraping aleatório.

Não criar Opportunity Engine nesta sprint.

---

# Próxima Sprint

SPRINT_03_OPPORTUNITY_ENGINE_DETAILED.md
