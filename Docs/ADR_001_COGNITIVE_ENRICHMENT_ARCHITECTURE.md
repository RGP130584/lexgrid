# ADR 001: Implementação da Arquitetura de Enriquecimento Cognitivo e Simulador Tributário

## Status
**Aprovado**

## Contexto
O ecossistema tributário brasileiro apresenta alta complexidade (leis federais, incentivos estaduais e regimes municipais). O LexGrid precisava evoluir de um diagnóstico cadastral simples para um motor de tomada de decisão executiva (CFO/CLO Digital). 

Os requisitos do usuário exigiam:
1. **Dados Concretos e Reais:** Custos tributários simulados em reais (R$) para os regimes do Simples Nacional, Lucro Presumido e Lucro Real, em vez de percentuais genéricos.
2. **Inteligência de Editais e Fomento:** Guias práticos ("como conseguir") e projetos elegíveis de enquadramento para incentivos como FINEP, EMBRAPII, Lei do Bem e editais estaduais (FAPs).
3. **Validação de Restrições:** Verificação rigorosa contra impeditivos tributários do Simples Nacional cruzando 100% dos CNAEs secundários.
4. **Análise da Reforma:** Um parecer técnico contábil estruturado e tabela comparativa sobre o período de transição híbrida do IBS/CBS (2026-2033).
5. **Dívida Ativa:** Integração de débitos fiscais em aberto perante a Procuradoria-Geral da Fazenda Nacional (PGFN).

## Decisão
Implementamos a arquitetura do motor de enriquecimento em duas frentes integradas:

### 1. Backend: CNPJ Enrichment Service
- Consolidamos as chamadas da PGFN via BrasilAPI (`https://brasilapi.com.br/api/pgfn/v1/{cnpj}`) no módulo `ReceitaClient` com fallback automático.
- Estruturamos regras de negócio cognitivas no `CNPJEnrichmentService` para cruzar o Capital Social, CNAE principal/secundários e UF com os requisitos de isenção de impostos e elegibilidade de fomento.
- Mapeamos a elegibilidade do Simples Nacional verificando dinamicamente a presença de atividades financeiras ou impeditivas em toda a lista de CNAEs secundários.

### 2. Frontend: Dashboard e Modal Cognitivo
- Desenvolvemos o componente de modal dinâmico centralizado (`selectedItem`) alimentado por uma base de metadados robusta em `src/app/page.tsx`, mapeando etapas práticas de submissão e exemplos reais de projetos.
- Substituímos cartões estáticos por tabelas de comparação financeira premium (faturamento, alíquotas efetivas, custos anuais e economia projetada).
- Adicionamos seções específicas para ações imediatas de planejamento tributário e o parecer de transição da Reforma de consumo (CBS/IBS).

## Consequências

### Positivas
- **Ação Imediata:** O usuário recebe um plano de ação pronto com links oficiais e sugestões de projetos, reduzindo a fricção de acesso a fomentos.
- **Transparência e Confiança:** A exibição do número exato de CNAEs secundários verificados aumenta a autoridade técnica do diagnóstico.
- **Blindagem na Transição:** O parecer técnico contábil instrui a empresa sobre o aproveitamento de créditos em serviços de nuvem e TI na Reforma.

### Neutras / Negativas
- **Dependência de APIs de Terceiros:** A consulta da PGFN e dados cadastrais dependem da estabilidade das APIs públicas (BrasilAPI/ReceitaWS).
- **Manutenção de Editais:** Os links de editais governamentais e critérios de programas estaduais de fomento exigirão atualizações periódicas de metadados no repositório.
