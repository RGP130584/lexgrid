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