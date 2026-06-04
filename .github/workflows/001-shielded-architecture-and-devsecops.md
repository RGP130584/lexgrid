# ADR 001: Adoção de Shielded Architecture, Zero Trust e CI/CD Automatizado

## Status
Aceito

## Contexto
O LexGrid é uma plataforma corporativa que lida com dados tributários sensíveis (SPED) e utiliza Inteligência Artificial Generativa. Inicialmente, as validações de qualidade e segurança dependiam de scripts manuais (ex: `.bat`, `.sh`, `pre-commit-hook.py`) e aprovações interativas do desenvolvedor. Esse modelo era suscetível a falhas humanas, não escalava em ambientes de CI/CD em nuvem e não fornecia rastreabilidade jurídica adequada para as operações da IA.

Precisávamos de um modelo de governança em 10 camadas que garantisse "Defesa em Profundidade" (Defense in Depth), desde o terminal do desenvolvedor até o ambiente produtivo.

## Decisão
Decidimos implementar o padrão **Shielded Architecture Template** com as seguintes definições técnicas:

1. **Substituição da Esteira Local (Camada 1):**
   - Depreciamos os scripts manuais interativos.
   - Adotamos o framework oficial `pre-commit` (`.pre-commit-config.yaml`).
   - O fluxo local agora é *Fail-Fast* binário: bloqueia instantaneamente commits que contenham credenciais hardcoded, má formatação (Ruff) ou injeções nocivas identificadas pelo `ai_code_guard.py`.

2. **CI/CD Militar na Nuvem (Camada 3):**
   - Migramos as pipelines para o padrão `.github/workflows/`.
   - Implementamos verificações bloqueantes para Frontend (NPM Audit) e Backend (PyTest).
   - Adotamos análise de Composição de Software (SCA) usando **Syft** (geração de SBOM) e **Grype** para varredura de CVEs, mitigando ataques de *Supply Chain*.

3. **Testes Ofensivos Dinâmicos (Camada 10 - Red Team):**
   - A pipeline de infraestrutura (`infra.yml`) sobe o ambiente Docker com *Kernel Hardening* (`read_only: true`, `cap_drop: ALL`).
   - Injeções automatizadas (`ransomware_simulation.py` e `injection_suite.py`) atacam a infraestrutura e a IA a cada Pull Request para garantir que os *Guardrails* não falhem silenciosamente.

4. **Governança de IA e Zero Trust (Camada 4 e 7):**
   - Implementação do `AIFirewall` para inspecionar todas as entradas e saídas do LLM.
   - Criação do `DataLineageTracker` para gerar logs com hashes criptográficos (SHA-256) das respostas da IA, criando uma trilha de auditoria fiduciária que mitiga riscos de alucinação e garante *Compliance* LGPD.

## Consequências

### Positivas:
- **Velocidade:** O desenvolvedor não precisa mais interagir manualmente com o terminal a cada commit. Ferramentas como o `Ruff` auto-corrigem o código.
- **Segurança Inerente:** Vulnerabilidades e senhas vazadas não chegam à branch `main`, pois são travadas tanto pelo pre-commit (local) quanto pelo Trivy/Grype/Gitleaks (nuvem).
- **Prontidão para Auditoria:** Com a SBOM gerada e os logs do `DataLineageTracker`, a arquitetura suporta auditorias jurídicas profundas, o que aumenta a confiança de clientes Enterprise.

### Negativas (Trade-offs Aceitos):
- Curva de aprendizado inicial da equipe para lidar com comandos Git como `stash` e `rebase` ao interagir com o GitHub Actions.
- Maior consumo de tempo nos Pull Requests devido à exaustiva bateria de testes de invasão e subida da infraestrutura completa no *runner* da nuvem.