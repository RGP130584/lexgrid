# 🛡️ LexGrid - Visão de Produto, Arquitetura & Motor de Enriquecimento

O **LexGrid** é uma plataforma corporativa e *on-premise* de alta performance voltada para **Inteligência de CNPJ**, **Auditoria de Conformidade (SPED)** e **Mapeamento de Oportunidades Tributárias**, operando sob uma infraestrutura de IA local e blindada por princípios de segurança rígidos.

O sistema atua de forma autônoma como um **CFO e CLO Digital**, realizando o cruzamento inteligente de obrigações acessórias, enquadramentos regulatórios e bases de dados do governo para otimizar a carga tributária de empresas sob o modelo de soberania de dados (*AI-on-Premise*).

---

## 📐 Arquitetura do Sistema e Serviços

O ecossistema é conteinerizado em microsserviços seguros via *Docker*, organizados da seguinte forma:

| Componente | Tecnologia | Porta Host | Função Estratégica |
| :--- | :--- | :--- | :--- |
| **Frontend Cognitivo** | Next.js 14, React, Tailwind CSS | `3003` | Painel Executivo de Oportunidades e Simulador Comparativo. |
| **API Backend Gateway** | FastAPI (Python 3.10) | `8003` | Motor de Clean Architecture, processamento cognitivo e rotas MCP. |
| **Cofre de Segredos** | HashiCorp Vault | `8203` | HSM em Software para injeção dinâmica de senhas em memória RAM. |
| **Memória Longa Relacional**| PostgreSQL 16 (Hardened) | `55433` | Armazenamento de logs estruturados, cadastros e obrigações. |
| **Memória Semântica** | Qdrant | `56333` | Banco de dados vetorial para contextualização semântica (RAG). |
| **Memória Curta (Cache)** | DragonflyDB | `56379` | Cache em memória de alta performance compatível com Redis. |
| **Provedor de IA (Cloud)** | API OpenAI/Groq (Adapter) | - | Chamadas cognitivas na nuvem via LLM Adapter estruturado. |

---

## 🔒 Shielded Architecture (Segurança e Zero Trust)

O LexGrid implementa regras de governança e blindagem ativa:
- **Least Privilege:** Os contêineres rodam sob usuários dedicados sem permissões administrativas (`lexgrid:lexgrid`).
- **Hardening de Kernel:** Extirpação de capacidades de SO (`cap_drop: ALL`) e prevenção de privilégios (`no-new-privileges:true`).
- **Políticas CORS e Ingestão:** Comunicação interna protegida por mTLS e regras rígidas de acesso e-CAC/PGFN.
- **Validação de Qualidade (Camada 1):** Pre-commit hooks e validações estáticas independentes antes do envio ao repositório git.

---

## 🚀 Módulos e Funcionalidades

1. **Oportunidades & Fomentos (CFO/CLO Autônomo)**:
   - Mapeamento dinâmico de recursos não reembolsáveis (FINEP, EMBRAPII, CNPq, FAPs estaduais).
   - Dicionário interativo com link oficial do portal de cada edital, passo a passo para submissão e lista de projetos elegíveis sugeridos.
   - Identificação de oportunidades de redução (créditos de ICMS, energia - TUST/TUSD, agro e PIS/COFINS monofásicos).
2. **Simulador Tributário Comparativo**:
   - Grade comparativa em valores monetários reais (R$) entre Simples Nacional, Lucro Presumido e Lucro Real.
   - Validação automatizada contra impeditivos legais em **100% dos CNAEs secundários** do CNPJ pesquisado.
   - Planejamento tributário imediato com ações administrativas de redução fiscal aplicáveis hoje.
3. **Análise da Nova Reforma Tributária**:
   - Parecer técnico emitido sob a ótica de um contador especialista em direito tributário.
   - Tabela comparativa de carga nominal Pré vs. Pós Reforma (IBS, CBS e Imposto Seletivo).
   - Plano de preparação contábil para o período híbrido (2026-2033).
4. **Compliance, Riscos & Fontes**:
   - Varredura e apresentação de débitos ativos consolidados junto à **Dívida Ativa da União (PGFN)**.
   - Status de conexão ativa e auditoria das fontes de consulta governamentais federais e estaduais.
5. **Módulos de IA Desacoplados (SaaS Cloud Tools)**:
   - Substituição completa da IA local (Ollama) por uma arquitetura orientada a serviços (Cloud Tools).
   - Camada de abstração centralizada (LLM Adapter) compatível com o padrão OpenAI (Groq, OpenAI, Anthropic, etc.).
   - Endpoints cognitivos independentes, rápidos e validados por schema estrito:
     - `POST /api/tools/analyze-risk`: Recebe dados financeiros e de chassi e gera pontuação de risco e parecer analítico.
     - `POST /api/tools/generate-swot`: Recebe CNPJ e riscos do sistema e gera os 4 quadrantes da Matriz SWOT (Forces, Weaknesses, Opportunities, Threats) em JSON.
     - `POST /api/tools/extract-ncm`: Extrai semântica de produtos e seus NCMs (8 dígitos) a partir de notas fiscais ou textos brutos.

   #### 🖥️ Exemplo de Integração no Frontend (React/Vue)
   ```javascript
   async function handleGerarSwot() {
       setLoading(true);
       try {
           const res = await fetch('/api/tools/generate-swot', {
               method: 'POST',
               headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify({
                   cnpjData: cliente.dadosCadastrais,
                   riscosMapeados: cliente.riscos
               })
           });
           const json = await res.json();
           if (json.success) {
               setSwotDashboard(json.data); // Atualiza a UI imediatamente com forces, weaknesses, opportunities, threats
           }
       } catch (error) {
           alert("Erro ao processar análise inteligente.");
       } finally {
           setLoading(false);
       }
   }
   ```

---

## ⚙️ Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Docker e Docker Compose instalados.
- WSL2 configurado (caso esteja no Windows).
- Python 3.10 ou superior.

### 2. Inicialização dos Contêineres
Na raiz do projeto, execute o build e a inicialização dos serviços em segundo plano:
```bash
docker compose up -d --build
```

### 3. URLs e Pontos de Acesso
- **Dashboard Web (Frontend):** `http://localhost:3003`
- **Documentação Interativa (Swagger Docs):** `http://localhost:8003/docs`
- **Painel do Vault (Segredos):** `http://localhost:8203` (Token de dev local: `lexgrid_temp_dev_token`)

---

## 🧪 Suíte de Testes e Qualidade

O LexGrid possui uma esteira rigorosa para verificar e validar a integridade estrutural e segurança do código:

```bash
# 1. Ativar ambiente virtual
python -m venv .venv
source .venv/Scripts/activate

# 2. Instalar dependências de dev
pip install -r requirements-dev.txt

# 3. Rodar a esteira local de qualidade (Linting, Imports e AI-Guard)
python scripts/quality/run_quality_pipeline.py

# 4. Executar smoke tests de banco de dados
python test_db.py
python test_endpoints.py
```

---
> *Desenvolvido para resiliência e conformidade máxima no cenário contábil brasileiro.*
