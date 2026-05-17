# Modelo de Ameaças (Threat Model) - LexGrid Layer 6

## 1. Movimentação Lateral e Abuso de Containers
**Vetor:** Atacante escapa do container da IA/Backend e busca credenciais.
**Mitigação (Hardening):** 
- Todos os containers do `docker-compose.yml` operam com `read_only: true`.
- Aplicação universal de `cap_drop: ALL` e `no-new-privileges:true`.
- Arquivos temporários roteados para partições efêmeras (`tmpfs`).

## 2. Exfiltração de Segredos
**Vetor:** Variáveis de ambiente (`.env`) contendo senhas vazadas via Github.
**Mitigação (Vault):**
- Adoção do HashiCorp Vault. Segredos trafegam apenas em memória utilizando o `VaultManager`.
- Token dinâmico e expiração de acessos ABAC (IA nunca tem acesso à classe 'secret').

## 3. Prompt Injection Resultando em RCE
**Vetor:** Usuário convence a IA a executar um script shell dentro da máquina anfitriã.
**Mitigação (Zero Trust & Process Protection):**
- IA é submetida ao `ZeroTrustEngine` que monitora padrões de `action="dump"` ou ações OS.
- Avaliação Contínua do `BehaviorAnalyzer`.

## 4. Vazamento de Base de Dados (LGPD)
**Vetor:** Acesso indevido aos volumes Docker expondo PII.
**Mitigação (Criptografia):** O `EncryptionManager` impõe Criptografia em Repouso Nível-Campo com AES-GCM (Chave mestre no Vault).