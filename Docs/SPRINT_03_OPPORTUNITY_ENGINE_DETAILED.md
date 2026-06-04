# SPRINT_03_OPPORTUNITY_ENGINE_DETAILED.md

# Sprint 03 — Opportunity Engine Detailed
Versão 1.0

## Objetivo

Construir o principal motor de geração de valor do LexGrid.

Esta sprint transforma um Company Profile em oportunidades financeiras concretas.

O objetivo não é apenas informar dados da empresa.

O objetivo é encontrar dinheiro.

---

# Resultado Esperado

Entrada:

Company Profile

Saída:

- Oportunidades tributárias
- Incentivos fiscais
- Programas de fomento
- Programas P&D
- Oportunidades energia
- Oportunidades agro
- Benefícios regionais

---

# Arquitetura

Company Profile
↓
Rules Engine
↓
Opportunity Engine
↓
Ranking Engine
↓
Scoring Engine
↓
Explainability Engine
↓
Executive Opportunity Report

---

# Estrutura de Diretórios

app/modules/opportunities/

Arquivos:

registry.py
rules.py
engine.py
ranking.py
scoring.py
explainability.py
models.py
service.py

---

# TASK-0301
## Incentives Registry

Objetivo:

Criar o catálogo central de oportunidades.

Categorias:

- Fiscal
- Tributário
- Energia
- Agro
- Inovação
- P&D
- Regional

---

# Fontes Prioritárias

ANEEL
FINEP
BNDES
EMBRAPII
SUFRAMA
CAPDA
MCTI
Lei do Bem
Lei de Informática

---

# Estrutura do Registro

id
name
description
category
state
sector
legal_basis
valid_from
valid_until
risk_level

---

# TASK-0302
## Rules Engine

Objetivo

Determinar elegibilidade.

Entradas:

- CNAE
- Estado
- Porte
- Segmento

Saída:

eligible = true/false

---

# Regras

LLM nunca decide.

Somente regras determinísticas.

---

# TASK-0303
## Opportunity Engine

Objetivo

Cruzar:

Empresa
+
Incentivos
+
Regras

Resultado:

Lista de oportunidades elegíveis.

---

# TASK-0304
## Ranking Engine

Objetivo

Ordenar oportunidades.

Critérios:

- impacto financeiro
- risco
- facilidade implementação
- prazo

---

# TASK-0305
## Scoring Engine

Objetivo

Gerar score.

Faixas:

LOW
MEDIUM
HIGH
CRITICAL

---

# TASK-0306
## Explainability Engine

Objetivo

Explicar:

- por que apareceu
- base legal
- documentação necessária
- próximos passos

---

# Endpoint

POST /api/v1/opportunities/analyze

Request:

{
 "cnpj":"00000000000191"
}

---

# Response

{
 "opportunities":[]
}

---

# PostgreSQL

Tabela:

opportunities

Campos:

id
company_id
opportunity_name
category
score
risk
created_at

---

# Dragonfly

Cache:

opportunities:{cnpj}

TTL:

12h

---

# Relatório Executivo

Cada oportunidade deve conter:

Nome
Descrição
Base Legal
Impacto Estimado
Score
Risco
Próximos Passos

---

# Testes

test_registry.py
test_rules.py
test_engine.py
test_scoring.py
test_ranking.py

---

# Critérios de Aceite

✓ Empresa analisada

✓ Oportunidades encontradas

✓ Ranking gerado

✓ Score gerado

✓ Explainability gerada

✓ Endpoint funcional

---

# Definition of Done

[ ] Registry criado
[ ] Rules Engine criado
[ ] Opportunity Engine criado
[ ] Ranking criado
[ ] Score criado
[ ] Explainability criada
[ ] Endpoint criado
[ ] Testes criados

---

# Anti-Padrões

Não usar GPT para decidir elegibilidade.

Não usar regras ocultas.

Não retornar oportunidade sem base legal.

Não retornar oportunidade sem explainability.

---

# Próxima Sprint

SPRINT_04_MVP_DEMONSTRAVEL_DETAILED.md
