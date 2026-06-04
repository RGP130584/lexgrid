# MASTER_EXECUTION_PLAN.md

# LexGrid — Master Execution Plan
Versão 1.0

## Objetivo
Construir uma plataforma soberana brasileira de inteligência corporativa baseada em IA para descoberta de oportunidades financeiras, tributárias, incentivos, fomentos e compliance através do CNPJ.

## Fluxo Principal

CNPJ
→ Enrichment Engine
→ Context Engine (CAG)
→ Opportunity Engine
→ Rules Engine
→ Reasoning Engine (RX)
→ RAG Tributário/Jurídico
→ Judge Engine
→ Governance Layer
→ Human Approval
→ Executive Report

---

# Princípios

- Business First
- Deterministic First
- Explainability First
- Governance First
- Human In The Loop
- Security By Design

---

# Arquitetura

lexgrid/
- app/
- scripts/
- infrastructure/
- knowledge/
- data/
- reports/
- tests/
- docs/
- docker-compose.yml
- pyproject.toml
- .env.example

---

# EPIC 00 — FOUNDATION

## Objetivo
Criar a fundação operacional.

### TASK-0001
Reorganização estrutural.

### TASK-0002
Bootstrap FastAPI.

### TASK-0003
Docker Compose.

### TASK-0004
Healthchecks.

---

# EPIC 01 — CNPJ INTELLIGENCE

## Objetivo
Transformar CNPJ em Company Profile.

### TASK-0101
CNPJ Validator.

### TASK-0102
Receita Connector.

### TASK-0103
Company Classifier.

### TASK-0104
Enrichment Engine.

---

# EPIC 02 — OPPORTUNITY INTELLIGENCE

## Objetivo
Encontrar oportunidades financeiras.

### TASK-0201
Incentives Registry.

### TASK-0202
Rules Engine.

### TASK-0203
Opportunity Engine.

### TASK-0204
Scoring Engine.

### TASK-0205
Explainability Engine.

---

# EPIC 03 — KNOWLEDGE PLATFORM

knowledge/
- tax
- legal
- incentives
- agro
- energy
- jurisprudence

### TASK-0301
Metadata Engine.

### TASK-0302
Knowledge Ingestion.

### TASK-0303
Versionamento.

---

# EPIC 04 — RAG

### TASK-0401
Embeddings Pipeline.

### TASK-0402
Qdrant Collections.

### TASK-0403
Retrieval Engine.

---

# EPIC 05 — CAG

### TASK-0501
Context Engine.

### TASK-0502
Context Builder.

---

# EPIC 06 — RX

### TASK-0601
Reasoning Engine.

### TASK-0602
Confidence Engine.

### TASK-0603
Recommendation Engine.

---

# EPIC 07 — JUDGE ENGINE

### TASK-0701
Grounding Validator.

### TASK-0702
Hallucination Detector.

### TASK-0703
Temporal Validator.

### TASK-0704
Risk Validator.

### TASK-0705
Compliance Validator.

---

# EPIC 08 — OSINT

Fontes:
- Receita
- ANEEL
- FINEP
- SUFRAMA
- ComprasGov
- Notícias
- Editais
- Tribunais

### TASK-0801
Source Connectors.

### TASK-0802
Crawl4AI.

### TASK-0803
Correlation Engine.

### TASK-0804
Trust Scoring.

---

# EPIC 09 — AGENTS

- CFO Agent
- Incentives Agent
- Governance Agent

Regra:
Agentes coordenam.
Engines decidem.

---

# EPIC 10 — EXECUTIVE DASHBOARD

- Consulta CNPJ
- Oportunidades
- Scores
- Riscos
- Relatórios
- Approval Gates

---

# EPIC 11 — TESTES E VALIDAÇÃO

Camadas:
1. Unit Tests
2. Integration Tests
3. E2E Tests
4. Tax Validation Suite
5. Judge Validation Suite
6. Security Suite

Meta:
- Cobertura mínima: 85%
- Cobertura ideal: 90%+

---

# Bootstrap Obrigatório

## docker-compose.yml
- backend
- postgres
- qdrant
- dragonfly
- ollama
- prometheus
- grafana

## pyproject.toml
- FastAPI
- Qdrant
- LangChain
- Ollama
- Ruff
- Black
- Mypy
- Pytest

## .env.example
- Banco
- Cache
- Vetor
- IA
- Segurança
- Observabilidade

---

# Definição de Pronto

Uma task só está concluída quando:
- Código implementado
- Testes criados
- Cobertura atingida
- Documentação atualizada
- Logs implementados
- Observabilidade ativa
- Segurança validada

---

# Resultado Esperado

O usuário informa um CNPJ.

O LexGrid:
- Enriquece os dados
- Consulta bases oficiais e OSINT
- Identifica oportunidades
- Valida legislação
- Impede hallucinations
- Explica conclusões
- Gera relatório executivo
- Mantém trilha de auditoria

