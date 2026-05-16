# ESTEIRA DE DESENVOLVIMENTO - LEXGRID

## Visão Geral
Pipeline automatizado que força validações de segurança, testes de banco de dados e aprovação manual antes de consolidar commits no Git.

## Fluxo do Processo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Desenvolvedor executa: git commit -m "mensagem"             │
└────────────────┬────────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. PRE-COMMIT HOOK ACIONADO AUTOMATICAMENTE                    │
│    ├─ Executa test_db.py (testa BD)                           │
│    ├─ Valida endpoints FastAPI                                 │
│    └─ Verifica vazamento de credenciais                        │
└────────────────┬────────────────────────────────────────────────┘
                 ↓
        ┌────────┴───────┐
        │                │
     [FALHA]         [SUCESSO]
        │                │
        ↓                ↓
   ❌ BLOQUEADO    ┌─────────────────────────────────────┐
   Corrija bug  │ 3. AGUARDANDO APROVACAO MANUAL       │
                 │    "Aguardando aprovacao do usuario" │
                 │    [a] Aprova                        │
                 │    [c] Cancela                       │
                 │    [r] Revisa                        │
                 └────────────┬────────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │ COMMIT CONSOLIDADO  │
                    │ ✓ Aprovado          │
                    └─────────────────────┘
```

## Componentes

### 1. **test_db.py** - Validação de Banco de Dados
Localização: `backend/test_db.py`

Testa:
- ✓ Conexão PostgreSQL
- ✓ Conexão Dragonfly (Redis)
- ✓ Conexão Qdrant
- ✓ Disponibilidade Ollama

**Execução manual:**
```bash
python backend/test_db.py
```

### 2. **pre-commit-hook.py** - Automação de Validação
Localização: `scripts/pre-commit-hook.py`

Executa automaticamente antes de commits:
1. Testes de banco de dados
2. Validação de API (FastAPI)
3. Verificação de credenciais
4. **Aguarda aprovação manual do desenvolvedor**

### 3. **SECURITY_REVIEW_PROMPT.md** - Instrução para ChatGPT Go
Localização: `.github/SECURITY_REVIEW_PROMPT.md`

Template para análise de segurança via AI:
- Detecção de vulnerabilidades OWASP Top 10
- Identificação de vazamentos de credenciais
- Validação de cobertura de testes
- Geração de recomendações

## Instalação da Esteira

### Passo 1: Instalar Git Hook Nativo
```bash
cd c:\Users\Ricardo\Documents\projetos\LexGrid\lexgrid

# Criar diretório de hooks (se não existir)
mkdir -p .git\hooks

# Criar arquivo pre-commit nativo (Windows)
# Salvar como .git/hooks/pre-commit (sem extensão)
```

### Passo 2: Conteúdo do Hook Nativo
Arquivo: `.git/hooks/pre-commit`
```bash
#!/bin/bash
python scripts/pre-commit-hook.py
exit $?
```

No Windows (PowerShell), usar:
Arquivo: `.git/hooks/pre-commit.ps1`
```powershell
python scripts/pre-commit-hook.py
exit $LASTEXITCODE
```

### Passo 3: Dar Permissão de Execução
```bash
chmod +x .git/hooks/pre-commit
```

## Como Usar

### Fluxo Normal de Desenvolvimento

```bash
# 1. Fazer alterações no código
code backend/main.py

# 2. Adicionar ao staging
git add backend/main.py

# 3. Tentar fazer commit
git commit -m "feat: novo endpoint de IA"

# 4. Hook executa automaticamente:
#    - Testa banco de dados
#    - Valida API
#    - Verifica credenciais
#    - Aguarda aprovacao manual
#
# 5. Responder no prompt:
#    Sua escolha (a/c/r): a
#
# 6. Commit consolidado! ✓
```

## Integração com ChatGPT Go (VS Code)

### Configurar ChatGPT Go para Análise de Segurança

1. Instalar ext ensão **ChatGPT Go** no VS Code
2. Abrir arquivo `.github/SECURITY_REVIEW_PROMPT.md`
3. No ChatGPT Go, usar comando:
   ```
   /review backend/main.py
   ```
4. IA analisará baseada nas regras de segurança

### Exemplo de Uso:
```
User: /review backend/mai.py

ChatGPT Go:
> Analisando backend/main.py...
>
> === ANALISE DE SEGURANCA - LEXGRID ===
> Data: 2026-05-16
> Arquivo(s): backend/main.py
>
> VULNERABILIDADES: NAO
> CREDENCIAIS VAZADAS: NAO
> COBERTURA TESTES: 85%
>
> STATUS: APROVADO
```

## Checklist de Segurança Automático

Antes de cada commit, o hook valida:

- [ ] Nenhuma credencial exposta
- [ ] Testes de BD passam
- [ ] FastAPI respondendo
- [ ] Sem padrões perigosos detectados
- [ ] ✓ Aprovação manual

## Troubleshooting

### Hook não executa
```bash
# Verificar se existe
ls -la .git/hooks/pre-commit

# Dar permissão
chmod +x .git/hooks/pre-commit

# Testar manualmente
python scripts/pre-commit-hook.py
```

### Erro: "Testes de banco de dados falharam"
```bash
# Verificar Docker containers rodando
docker compose -f backend/docker-compose.yml up -d

# Reexecutar testes
python backend/test_db.py
```

### Erro: "FastAPI nao respondeu"
```bash
# Iniciar servidor
cd lexgrid
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

## Fluxo com Ressalvas

Se encontrado:
- Vulnerabilidades MEDIA/ALTA (não CRITICA)
- Cobertura de testes 70-79%

Mensagem aparece: **"Commit bloqueado com ressalvas"**
- Developer pode corrigir
- Ou prosseguir com aprovação explícita no prompt

## Cmdtos Úteis

```bash
# Executar testes manualmente
python backend/test_db.py

# Rodar hook manualmente
python scripts/pre-commit-hook.py

# Bypassar hook (último recurso - não recomendado)
git commit --no-verify -m "mensagem"

# Ver status dos testes
git diff --cached --name-only
```

---

**Última atualização:** 2026-05-16
**Responsável:** LexGrid DevOps
