# LEXGRID - INSTRUÇÃO DE CODE REVIEW DE SEGURANÇA PARA GPT

## OBJETIVO
Validar código antes de commits analisando vulnerabilidades críticas e vazamento de credenciais.

## REGRAS DE ANÁLISE OBRIGATÓRIA

### 1. VULNERABILIDADES OWASP TOP 10
Verificar e reportar:
- ✓ **A01:2021 - Broken Access Control**: Falta de autorização/autenticação
- ✓ **A02:2021 - Cryptographic Failures**: Dados sensíveis em texto plano
- ✓ **A03:2021 - Injection**: SQL Injection, Command Injection, Template Injection
- ✓ **A04:2021 - Insecure Design**: Falta de autenticação, rate limiting, validação
- ✓ **A05:2021 - Security Misconfiguration**: Configurações inseguras, debug ativo
- ✓ **A06:2021 - Vulnerable Components**: Dependências desatualizadas
- ✓ **A07:2021 - Authentication Failures**: Senhas fracas, sessões inseguras
- ✓ **A08:2021 - Data Integrity Failures**: CSRF, validação inadequada
- ✓ **A09:2021 - Logging & Monitoring**: Falta de logs de segurança
- ✓ **A10:2021 - SSRF**: Server-Side Request Forgery

### 2. VAZAMENTO DE CREDENCIAIS
Procurar e ALERTAR se encontrado:
- [ ] Strings com "password", "secret", "api_key", "token" em código
- [ ] URLs PostgreSQL/Redis/Qdrant com credenciais hardcoded
- [ ] Arquivos .env expostos no git
- [ ] AWS Keys, API Keys privadas, JWT secrets
- [ ] Database connection strings com credenciais
- [ ] OAuth tokens ou Bearer tokens

### 3. COBERTURA DE TESTES
Validar:
- [ ] Arquivo test_db.py existe e testa conexões
- [ ] Testes de FastAPI API endpoints
- [ ] Testes de autenticação/autorização
- [ ] Testes de validação de entrada
- [ ] Mínimo 80% de cobertura em código crítico

### 4. PADRÃO DE RESPOSTA OBRIGATÓRIO

```
=== ANALISE DE SEGURANCA - LEXGRID ===
Data: [DATA]
Arquivo(s) analisado(s): [LISTAGEM]

VULNERABILIDADES ENCONTRADAS: [SIM/NAO]
[Se SIM, listar cada uma com severity: CRITICA/ALTA/MEDIA/BAIXA]

VAZAMENTO DE CREDENCIAIS: [SIM/NAO]
[Se SIM, listar arquivos/linhas comprometidas]

COBERTURA DE TESTES: [PERCENTUAL]%
[Detalhes de gaps identificados]

RECOMENDACOES:
1. [Ação corretiva prioritária]
2. [Ação corretiva secundária]

STATUS FINAL: [APROVADO COM RESSALVAS / NAO APROVADO / APROVADO]
===
```

### 5. CRITÉRIO DE BLOQUEIO
O commit é AUTOMATICAMENTE BLOQUEADO se:
- Encontrar vulnerabilidade CRITICA (sem exceção)
- Detectar credenciais expostas
- Cobertura de testes < 70%

O commit pode prosseguir COM APROVAÇÃO DO DESENVOLVEDOR se:
- Vulnerabilidades ALTA/MEDIA com plano de remediação
- Cobertura de testes entre 70-79%

## COMO USAR COM CHATGPT GO

1. Cole o conteúdo dos arquivos modificados
2. Execute: `/review [arquivo.py]`
3. Aguarde análise automática
4. Se bloqueado: Corrija e resubmeta
5. Se com ressalvas: Aguarde aprovação do usuário

## EXCLUSÕES PERMITIDAS
- Arquivos de configuração (*.yml, *.json, *.env.example)
- Documentação (*.md)
- Testes unitários (test_*.py)
- Arquivos gerados automaticamente
