<<<<<<< HEAD
# Documento de Visão: Lexgrid — Versão 5.0 (Arquitetura, MCP & Segurança)

**Data:** 16 de Maio de 2026  
**Responsável:** Ricardo Gabriel  

## 1. Introdução e Propósito
Este documento detalha a visão estratégica, técnica e operacional do projeto Lexgrid (anteriormente TaxAI Brasil). O objetivo é estabelecer uma plataforma de inteligência corporativa e pessoal de alta performance, operando em regime 100% on-premise (local). O sistema atua como um CFO e CLO autônomo, focado na malha de conexões (Grid) e na legislação (Lex) do complexo ecossistema tributário brasileiro.

## 2. Descrição do Problema e Oportunidade
O cenário tributário e jurídico brasileiro é caracterizado por burocracia extrema e layouts engessados (SPED). Empresas perdem bilhões em créditos não recuperados. O Lexgrid resolve isso com processamento local soberano, automação executiva e OSINT profundo.

## 3. Arquitetura do Ecossistema (Core Engine)
A arquitetura segue o conceito de "Sleeper Build", blindada e padronizada pelo Model Context Protocol (MCP).

| Componente | Tecnologia | Função Estratégica |
| :--- | :--- | :--- |
| **Gateway Backend** | FastAPI (Python) | Micro-framework de alta velocidade e TDD obrigatório. |
| **Protocolo de Ferramentas** | Model Context Protocol (MCP) | Padroniza a comunicação da IA com APIs e bases locais. |
| **Orquestração** | Temporal Server + LangGraph | Gestão de fluxos de trabalho entre os agentes especialistas. |
| **Bancos de Dados** | Qdrant / PostgreSQL / DragonflyDB | Armazenamento vetorial, relacional e cache em memória. |

## 4. Módulos de Inteligência Detalhados
- **Módulo Fiscal (O CFO Autônomo):** Recuperação de ativos (TUST/TUSD) e auditoria de arquivos magnéticos do governo via ingestão segura.
- **Módulo Jurídico e Societário (O CLO Autônomo):** Análise de risco, descoberta de malhas societárias e estruturação patrimonial fiduciária.

## 5. Aceleradores Estratégicos e Arsenal Open-Source
### 5.1 Base Global de Agentes (Infraestrutura)
- **mcp-server-builder & c-level-advisor:** Geração automática de MCPs e injeção de persona executiva.
- **Prism Scanner:** Auditoria de segurança local contra código malicioso.

### 5.2 Arsenal Nacional e Deep OSINT Fiscal
- **sped-br/python-sped:** Biblioteca injetada via MCP para o Agente CFO realizar a ingestão, leitura e validação autônoma de arquivos SPED.
- **SINARC:** Motor de OSINT utilizando teoria dos grafos para desenhar relações societárias a partir de CNPJs.
- **Crawl4AI + mcp-crawl4ai-rag:** Web scraper imune a bloqueios, utilizado para extrair editais e portais governamentais.

## 6. Esteira de Desenvolvimento e Segurança (CI/CD Local)
O desenvolvimento do Lexgrid é protegido por uma pipeline rigorosa que força validações antes da consolidação de qualquer código no repositório.

- **6.1 Fluxo de Validação (Pre-Commit Hook):** Validações de conexão (PostgreSQL, Dragonfly, Qdrant, Ollama), responsividade da API FastAPI e verificação de vazamento de credenciais.
- **6.2 Auditoria de Código via IA (ChatGPT Go):** Utilização do `SECURITY_REVIEW_PROMPT.md` para análise de vulnerabilidades OWASP Top 10 e cobertura de testes (> 85%).
- **6.3 Controle Fiduciário:** O commit só é consolidado após a esteira aprovar todos os testes e o desenvolvedor inserir ativamente a aprovação manual.

## 7. Roadmap de Implementação Atualizado
**Fase 1:** Infraestrutura Core — VS Code, `.cline/rules`, containers (Postgres/Qdrant/Dragonfly) e ativação da Esteira de CI/CD. *(Concluído)*  
**Fase 2:** O Motor Brasil — Ativação do Crawl4AI e integração do `python-sped` para leitura de obrigações acessórias. *(Concluído)*  
**Fase 3:** Inteligência Societária — Implementação do SINARC para mapeamento de Holdings.
=======
# 🛡️ LexGrid - Corporate AI & Motor de Enriquecimento

O **LexGrid** é uma plataforma corporativa avançada focada em **Inteligência de CNPJ** e **Oportunidades Tributárias (SPED)**, suportada por uma arquitetura de IA local e blindada sob os mais rígidos princípios de segurança.

---

## 📐 Arquitetura do Sistema

O projeto foi concebido utilizando uma arquitetura conteinerizada (*Docker*), baseada em microsserviços e **Zero Trust**.

| Componente | Tecnologia | Porta Host | Função |
| :--- | :--- | :--- | :--- |
| **Frontend Cognitivo** | Next.js 14, React, Tailwind | `3003` | Painel Executivo do LexGrid. |
| **API Backend** | FastAPI (Python 3.10) | `8003` | Motor central, Clean Architecture e fluxos de IA. |
| **Cofre de Segredos** | HashiCorp Vault | `8203` | HSM em Software para injeção dinâmica de senhas. |
| **Memória Longa** | PostgreSQL 16 | `55433` | Armazenamento relacional e transacional. |
| **Memória Semântica** | Qdrant | `56333` | Banco vetorial para RAG (Recuperação de Informação). |
| **Memória Curta** | Dragonfly | `56379` | Cache de altíssima performance (compatível com Redis). |
| **Motor de IA Local** | Ollama | `51434` | Execução de LLMs open-source 100% On-Premise. |

---

## 🔒 Shielded Architecture (Segurança em 1º Lugar)

O LexGrid adota estritamente os princípios do **Shielded Architecture Template**:
- **Zero Trust & Least Privilege:** Nenhum container roda como `root`. Aplicação e Front end rodam com usuários restritos (`lexgrid:lexgrid`).
- **Hardening de Kernel:** Todos os containers possuem extirpação de capacidades (`cap_drop: ALL`) e prevenção de escalonamento (`no-new-privileges:true`).
- **Prevenção OWASP:** Políticas de CORS restritas (sem wildcard `*`) no backend e limitação de rotas.
- **Integração Contínua Blindada:** Pipeline com 8 fases no GitHub Actions incluindo *Secret Scanning* (Gitleaks), *Container Scan* (Trivy), e *SAST* (Bandit).

Para ler a política de arquitetura oficial completa, consulte: `docs/manual/secure-architecture.md`.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Docker e Docker Compose instalados.
- WSL2 configurado (para usuários de Windows).
- Python 3.10 (opcional, para testes locais e *pre-commits*).

### 2. Subindo a Infraestrutura
Na raiz do projeto, construa e inicie os containers em segundo plano:

```bash
docker compose up -d --build
```

### 3. Acessando os Serviços
- **Dashboard Web (Next.js):** http://localhost:3003
- **Documentação Interativa da API (Swagger):** http://localhost:8003/docs
- **Interface do Vault:** http://localhost:8203 (Token local de dev: `lexgrid_temp_dev_token`)

### 4. Modo de Desenvolvimento (Hot-Reload)
A infraestrutura está configurada para mapear os arquivos locais de código-fonte para dentro dos containers. 
Qualquer alteração em `lexgrid/` (Python) ou em `frontend/` (Next.js) será recarregada automaticamente na API e no Front end, sem a necessidade de reiniciar o Docker.

---

## 🧪 Testes e Validação de Infraestrutura

O LexGrid conta com scripts rigorosos para testar a comunicação entre as diferentes camadas de memória (*Relacional e Semântica*). Para executá-los em seu ambiente local usando o interpretador do seu host:

```bash
# Crie e ative seu ambiente virtual Python
python -m venv .venv
source .venv/Scripts/activate  # (No Windows PowerShell)

# Instale as dependências de desenvolvimento
pip install -r requirements-dev.txt

# Execute o validador de Banco de Dados e Vetorial
python test_db.py
```

---

## 📑 Estrutura de Diretórios Principal

```text
lexgrid/
├── frontend/          # Aplicação Web (Next.js, TailwindCSS)
├── app/               # Regras de Negócio e Rotas da API Backend (FastAPI)
├── tests/             # Suíte de testes unitários e de integração
├── ci.yml, infra.yml  # Workflows automatizados de CI/CD e Qualidade
├── docker-compose.yml # Malha de serviços e infraestrutura local segura
└── main.py            # Ponto de entrada da API Backend
```

> *Desenvolvido para máxima resiliência corporativa. Nunca confie. Sempre verifique.*
>>>>>>> 2a3d070 (chore: reestruturação de pastas, frontend e ativação da esteira pre-commit)
