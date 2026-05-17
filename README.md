# Plataforma corporativa e on-premise especializada em inteligência tributária e automação executiva focada na malha legislativa brasileira.

O LexGrid atua de forma autônoma (como CFO e CLO digitais) visando a recuperação massiva de créditos e a mineração de dados em obrigações estruturadas (SPED, ECD, ECF), preservando rigorosamente o sigilo corporativo. Trata-se de uma arquitetura baseada em governança, segurança fiduciária e execução 100% local, blindando as informações estratégicas da empresa sob o modelo AI-on-Premise.

## 3. Arquitetura em Camadas
- **Camada 1 (Qualidade & CI Local):** Conjunto estático e veloz de validações (Ruff, Black, Mypy, Bandit) e proteções proativas contra injeção de código inseguro ou vazamento de segredos, independentemente do Docker estar ativo.
- **Camada 2 (Zelador Dev):** Auto-healing e gerenciamento inteligente da infraestrutura.
- **Camada 3 (CI/CD Militar):** Pipeline Zero Trust hospedada no GitHub Actions com SBOM.
- **Camada 4 (AI Security & Governance):** Firewall de IA, Guardrails, PII Sanitization.
- **Camada 5 (Auditoria, Observabilidade e Forensics):** SIEM nativo, Tracing Distribuído (OpenTelemetry), Digital Forensics e logs imutáveis.
- **Camada 6 (Zero Trust & Cyber Defense):** Least Privilege, ABAC, Hardening de containers (read-only FS), HashiCorp Vault para secrets e mTLS.
- **Camada 7 (Data Governance & Resilience):** Backup Automático, Disaster Recovery (RTO/RPO), Data Lineage, Purge LGPD e Validação de Integridade.
- **Camada 8 (AI Ops & MLOps Governance):** Model Registry, Prompt Versioning, Drift Detection, Embeddings Poisoning Defense, AI Cost Tracking.
- **Camada 9 (Core Backend):** API em FastAPI, LangChain, Agentes e integrações de negócio.
- **Camada 10 (Red Team & Chaos Engineering):** Validação de Resiliência, Prompt Injection automatizado, Simulação de Ransomware e Docker Breakout Tests.

> **Novidade (MVP Etapa 1 & 2):** O "CNPJ Enrichment Engine" e o "Opportunity Engine" foram implementados. Juntos, recebem CNPJs, enriquecem os dados cadastrais, e cruzam regras tributárias complexas para gerar um ranking de Oportunidades Financeiras com potencial executivo, score e Explainability.

## 4. Estrutura do Projeto
```text
lexgrid/
│
├── app/
│   ├── api/
│   │   ├── routers/      # Rotas FastAPI isoladas
│   │   └── schemas/      # Validadores e representações Pydantic
│   ├── modules/          # Domínios de negócio (cnpj, tax, energy, etc)
│   ├── services/         # Integrações (ai, scraping, enrichment, rag, ocr)
│   ├── engines/          # Motores Inteligentes (opportunity_engine, tax_engine)
│   ├── repositories/     # Adaptadores de Banco de Dados e Cache
│   ├── models/           # DTOs, value_objects e entities DDD
│   ├── core/             # Configurações, Segurança e Logging Globais
│   └── utils/
│
├── scripts/              # Ferramentas independentes e auxiliares
│   ├── dev/
│   ├── security/
│   ├── zelador/          # Agent autônomo de DevSecOps e infra
│   ├── migration/
│   ├── backup/
│   ├── seed/
│   ├── testing/
│   └── observability/
│
├── infrastructure/       # Configurações para deploy isolado e infra on-prem
│   ├── docker/
│   ├── postgres/
│   ├── qdrant/
│   ├── vault/
│   └── grafana/
│
├── data/                 # Raw data, backups, snapshots (ignorados no git)
├── knowledge/            # Bases de conhecimento tributárias, docs e pdfs (RAG)
├── reports/              # Saídas de auditoria e geração de relatórios
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── security/
│   ├── ai/
│   └── performance/
│
├── docs/                 # Documentação de Arquitetura, API e Modelagem
├── .github/
│   ├── workflows/
│   └── CODEOWNERS
│
├── docker-compose.yml    # Root entrypoint para Infra Estruturada
├── pyproject.toml        # Configuração das dependências (Ruff, MyPy)
├── README.md
└── .env.example
```

## 5. Como Rodara

```

## 6. Como Desenvolver
1. Crie seu virtual environment na pasta raiz e instale as dependências: `pip install -r requirements-dev.txt`
2. Habilite a esteira de desenvolvimento segura (Camada 1):
```bash
pre-commit install
```

## 7. Como Executar Qualidade (Manualmente)
Valida estaticamente segurança, imports, formatação e anomalias de AI, **sem** dependência do banco de dados:
```

Agente focado em auto-healing e telemetria profunda da Camada 3:
```bash
# Checkup estático manual:
python scripts/zelador.py

# Executar em modo Daemon 24/7 (Recovery Activo):
python scripts/zelador.py --daemon
``
## 10. Roadmap Evolutivo
*   **Fase 1:** Arquitetura DevSecOps desacoplada (Camada 1 veloz). (Concluído)
*   **Fase 2:** Integração do MCP SPED para consumo unificado.
*   **Fase 3:** Refinamento do Agente Societário via Grafos no frontend cognitivo.