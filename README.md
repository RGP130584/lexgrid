# Documento de Visão e Arquitetura: LexGrid — Versão 5.0 (Corporate AI & Motor de Enriquecimento)

**Data:** 16 de Maio de 2026  
**Responsável:** Ricardo Gabriel  

O **LexGrid** (anteriormente TaxAI Brasil) é uma plataforma corporativa avançada focada em **Inteligência de CNPJ** e **Oportunidades Tributárias (SPED)**, suportada por uma arquitetura de IA local e blindada sob os mais rígidos princípios de segurança. O objetivo é estabelecer uma plataforma de inteligência corporativa e pessoal de alta performance, operando em regime 100% on-premise (local). O sistema atua como um CFO e CLO autônomo, focado na malha de conexões (Grid) e na legislação (Lex) do complexo ecossistema tributário brasileiro.

## 1. Descrição do Problema e Oportunidade
O cenário tributário e jurídico brasileiro é caracterizado por burocracia extrema e layouts engessados (SPED). Empresas perdem bilhões em créditos não recuperados. O Lexgrid resolve isso com processamento local soberano, automação executiva e OSINT profundo.

## 2. Arquitetura do Sistema e Ecossistema Core

O projeto foi concebido utilizando uma arquitetura conteinerizada (*Docker*), baseada em microsserviços e **Zero Trust** (conceito "Sleeper Build", blindada e padronizada pelo Model Context Protocol (MCP)).

| Componente | Tecnologia | Porta Host | Função Estratégica |
| :--- | :--- | :--- | :--- |
| **Frontend Cognitivo** | Next.js 14, React, Tailwind | `3003` | Painel Executivo do LexGrid. |
| **API Backend (Gateway)** | FastAPI (Python 3.10) | `8003` | Motor central, Clean Architecture, fluxos de IA de alta velocidade e TDD obrigatório. |
| **Cofre de Segredos** | HashiCorp Vault | `8203` | HSM em Software para injeção dinâmica de senhas. |
| **Protocolo de Ferramentas** | Model Context Protocol (MCP) | - | Padroniza a comunicação da IA com APIs e bases locais. |
| **Orquestração** | Temporal Server + LangGraph | - | Gestão de fluxos de trabalho entre os agentes especialistas. |
| **Memória Longa** | PostgreSQL 16 | `55433` | Armazenamento relacional e transacional. |
| **Memória Semântica** | Qdrant | `56333` | Banco vetorial para RAG (Recuperação de Informação). |
| **Memória Curta** | Dragonfly | `56379` | Cache de altíssima performance em memória (compatível com Redis). |
| **Motor de IA Local** | Ollama | `51434` | Execução de LLMs open-source 100% On-Premise. |

## 3. Módulos de Inteligência Detalhados
- **Módulo Fiscal (O CFO Autônomo):** Recuperação de ativos (TUST/TUSD) e auditoria de arquivos magnéticos do governo via ingestão segura.
- **Módulo Jurídico e Societário (O CLO Autônomo):** Análise de risco, descoberta de malhas societárias e estruturação patrimonial fiduciária.

## 4. Aceleradores Estratégicos e Arsenal Open-Source
### 4.1 Base Global de Agentes (Infraestrutura)
- **mcp-server-builder & c-level-advisor:** Geração automática de MCPs e injeção de persona executiva.
- **Prism Scanner:** Auditoria de segurança local contra código malicioso.

### 4.2 Arsenal Nacional e Deep OSINT Fiscal
- **sped-br/python-sped:** Biblioteca injetada via MCP para o Agente CFO realizar a ingestão, leitura e validação autônoma de arquivos SPED.
- **SINARC:** Motor de OSINT utilizando teoria dos grafos para desenhar relações societárias a partir de CNPJs.
- **Crawl4AI + mcp-crawl4ai-rag:** Web scraper imune a bloqueios, utilizado para extrair editais e portais governamentais.

## 5. Shielded Architecture (Segurança em 1º Lugar)

O LexGrid adota estritamente os princípios do **Shielded Architecture Template**:
- **Zero Trust & Least Privilege:** Nenhum container roda como `root`. Aplicação e Front end rodam com usuários restritos (`lexgrid:lexgrid`).
- **Hardening de Kernel:** Todos os containers possuem extirpação de capacidades (`cap_drop: ALL`) e prevenção de escalonamento (`no-new-privileges:true`).
- **Prevenção OWASP:** Políticas de CORS restritas (sem wildcard `*`) no backend e limitação de rotas.
- **Integração Contínua Blindada:** Pipeline com 8 fases no GitHub Actions incluindo *Secret Scanning* (Gitleaks), *Container Scan* (Trivy), e *SAST* (Bandit).

Para ler a política de arquitetura oficial completa, consulte: `docs/manual/secure-architecture.md`.

## 6. Como Executar o Projeto Localmente

### 6.1 Pré-requisitos
- Docker e Docker Compose instalados.
- WSL2 configurado (para usuários de Windows).
- Python 3.10 (opcional, para testes locais e *pre-commits*).

### 6.2 Subindo a Infraestrutura
Na raiz do projeto, construa e inicie os containers em segundo plano:

```
docker compose up -d --build
```

### 6.3 Acessando os Serviços
- **Dashboard Web (Next.js):** http://localhost:3003
- **Documentação Interativa da API (Swagger):** http://localhost:8003/docs
- **Interface do Vault:** http://localhost:8203 (Token local de dev: `lexgrid_temp_dev_token`)

### 6.4 Modo de Desenvolvimento (Hot-Reload)
A infraestrutura está configurada para mapear os arquivos locais de código-fonte para dentro dos containers. 
Qualquer alteração em `lexgrid/` (Python) ou em `frontend/` (Next.js) será recarregada automaticamente na API e no Front end, sem a necessidade de reiniciar o Docker.

## 7. Esteira de Desenvolvimento e Segurança (CI/CD Local)
O desenvolvimento do Lexgrid é protegido por uma pipeline rigorosa que força validações antes da consolidação de qualquer código no repositório.

- **Fluxo de Validação (Pre-Commit Hook):** Validações de conexão (PostgreSQL, Dragonfly, Qdrant, Ollama), responsividade da API FastAPI e verificação de vazamento de credenciais.
- **Auditoria de Código via IA (ChatGPT Go):** Utilização do `SECURITY_REVIEW_PROMPT.md` para análise de vulnerabilidades OWASP Top 10 e cobertura de testes (> 85%).
- **Controle Fiduciário:** O commit só é consolidado após a esteira aprovar todos os testes e o desenvolvedor inserir ativamente a aprovação manual.

O LexGrid conta com scripts rigorosos para testar a comunicação entre as diferentes camadas de memória (*Relacional e Semântica*). Para executá-los em seu ambiente local usando o interpretador do seu host:

```
# Crie e ative seu ambiente virtual Python
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências de desenvolvimento
pip install -r requirements-dev.txt

# Execute o validador de Banco de Dados e Vetorial
python test_db.py
```

## 8. Estrutura de Diretórios Principal

```text
lexgrid/
├── frontend/          # Aplicação Web (Next.js, TailwindCSS)
├── backend/           # Regras de Negócio e Rotas da API Backend (FastAPI)
├── tests/             # Suíte de testes unitários e de integração
├── scripts/           # Scripts de esteira e automação
├── docker-compose.yml # Malha de serviços e infraestrutura local segura
```

> *Desenvolvido para máxima resiliência corporativa. Nunca confie. Sempre verifique.*

## 9. Roadmap de Implementação Atualizado
**Fase 1:** Infraestrutura Core — VS Code, `.cline/rules`, containers (Postgres/Qdrant/Dragonfly) e ativação da Esteira de CI/CD. *(Concluído)*
**Fase 2:** O Motor Brasil — Ativação do Crawl4AI e integração do `python-sped` para leitura de obrigações acessórias. *(Concluído)*
**Fase 3:** Inteligência Societária — Implementação do SINARC para mapeamento de Holdings.
