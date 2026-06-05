import httpx
import os
from typing import List, Dict, Any

class SWOTMitigationEngine:
    @classmethod
    def build_swot(
        cls,
        cnpj: str,
        capital_social: float,
        divida_ativa: List[Dict[str, Any]],
        lawsuits: List[Dict[str, Any]],
        cyber_risks: Dict[str, Any],
        market_risks: Dict[str, Any],
        cnae_principal: str,
        regime_simulacao: Dict[str, Any],
        uf: str,
        protestos: List[Dict[str, Any]] = []
    ) -> Dict[str, List[str]]:
        """
        Gera a Matriz SWOT de forma estruturada e condicional (MVP).
        """
        forcas = []
        fraquezas = []
        oportunidades = []
        ameacas = []

        # --- 1. FORÇAS ---
        if capital_social >= 1000000.0:
            forcas.append("Forte estrutura de capital social declarado, aumentando a robustez perante credores.")
        if not divida_ativa:
            forcas.append("Regularidade fiscal plena perante a Dívida Ativa da União (PGFN).")
        if not lawsuits:
            forcas.append("Ausência de contingências ou litígios judiciais ativos cíveis ou trabalhistas.")
        if uf:
            forcas.append(f"Regularidade cadastral estabelecida na unidade federativa de origem ({uf}).")
        if not cyber_risks.get("vulnerabilidades_ciberneticas"):
            forcas.append("Perímetro cibernético externo limpo, sem portas críticas expostas publicamente.")
        if not protestos:
            forcas.append("Ausência de protestos em cartórios (CENPROT), indicando boa reputação cadastral comercial.")

        # Garantir pelo menos uma força
        if not forcas:
            forcas.append("Empresa em atividade com cadastro regularizado perante os órgãos competentes.")

        # --- 2. FRAQUEZAS ---
        if divida_ativa:
            fraquezas.append("Presença de débitos fiscais ativos inscritos na PGFN, com risco de execução patrimonial.")
        if lawsuits:
            fraquezas.append(f"Litígios ativos em andamento ({len(lawsuits)} processo(s) localizado(s)), gerando passivos contingentes.")
        
        vulns = cyber_risks.get("vulnerabilidades_ciberneticas", [])
        for v in vulns:
            fraquezas.append(f"Risco Cibernético: Serviço exposto na porta {v.get('porta')} ({v.get('servico')}) classificado como {v.get('criticidade')}.")
            
        leaks = cyber_risks.get("leaks_detectados", [])
        if leaks:
            fraquezas.append("Exposição operacional por vazamento de arquivos sensíveis indexados em indexadores públicos.")
            
        if capital_social < 50000.0:
            fraquezas.append("Baixa capitalização declarada, o que pode limitar a captação de recursos comerciais ou fomento.")
        if protestos:
            fraquezas.append("Inadimplência formalizada identificada (Títulos Protestados ativos). Risco de bloqueio de crédito na praça.")

        # Garantir pelo menos uma fraqueza se estiver tudo saudável (para dar feedback construtivo)
        if not fraquezas:
            fraquezas.append("Dependência de processos manuais para monitoramento preventivo de riscos fiscais recorrentes.")

        # --- 3. OPORTUNIDADES ---
        is_rd_tech = any(cnae_principal.startswith(prefix) for prefix in ["62", "63", "72", "20", "26"])
        
        if is_rd_tech:
            oportunidades.append("Habilitação para o benefício fiscal da Lei do Bem, com exclusão tributária em IRPJ/CSLL.")
            oportunidades.append("Acesso a recursos não reembolsáveis de fomento à inovação da FINEP e EMBRAPII.")
            oportunidades.append("Financiamento subsidiado via BNDES Finame Inovação para licenciamento de softwares.")
            
        if regime_simulacao.get("regimes", {}).get("simples_nacional", {}).get("elegivel", False) and is_rd_tech:
            oportunidades.append("Otimização tributária imediata via Fator R (redução do Simples do Anexo V de 15,5% para 6% no Anexo III).")
            
        if any(cnae_principal.startswith(p) for p in ["10", "20", "26", "28", "29", "30", "35"]) or capital_social >= 500000.0:
            oportunidades.append("Recuperação judicial/administrativa de ICMS cobrado indevidamente sobre tarifas de transmissão de energia (TUST/TUSD).")
            
        if any(cnae_principal.startswith(p) for p in ["45", "47", "56"]): # Comércio e alimentação
            oportunidades.append("Recuperação retrospectiva e segregação de receitas monofásicas de PIS/COFINS (PIS/COFINS Monofásico).")
            
        if uf == "AM":
            oportunidades.append("Aproveitamento de incentivos fiscais estaduais (ICMS estimulado) e federais na Zona Franca de Manaus (SUFRAMA/CAPDA).")

        if not oportunidades:
            oportunidades.append("Revisão semestral preventiva de enquadramento tributário para redução de custos fiscais gerais.")

        # --- 4. AMEAÇAS ---
        selic = market_risks.get("taxa_selic", 10.5)
        pressao = market_risks.get("pressao_setorial", "").upper()
        
        if selic > 10.0:
            ameacas.append(f"Custo financeiro de captação de crédito elevado devido à taxa Selic fixada em {selic}%.")
        if "ALTA" in pressao or "MÉDIA" in pressao:
            ameacas.append(f"Arrefecimento de demanda setorial macroeconômica ({pressao.lower()}) impactando fluxo de caixa.")
            
        ameacas.append("Complexidade operacional decorrente da transição híbrida da Reforma Tributária (IVA Dual CBS/IBS) de 2026 a 2033.")
        
        # Imposto seletivo
        if any(cnae_principal.startswith(p) for p in ["11", "12", "29", "06"]): # bebidas, fumo, automotivo, extração
            ameacas.append("Majoração de custos de insumos ou produtos sob incidência do novo Imposto Seletivo pós-reforma.")

        return {
            "forcas": forcas,
            "fraquezas": fraquezas,
            "oportunidades": oportunidades,
            "ameacas": ameacas
        }

    @classmethod
    async def generate_mitigation_opinion(
        cls,
        cnpj: str,
        scores: Dict[str, float],
        swot: Dict[str, List[str]],
        capital_social: float
    ) -> str:
        """
        Orquestra a geração do Parecer de Mitigação:
        Tenta usar o Ollama local e, se indisponível, aplica um fallback estático robusto.
        """
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        
        # Garante o esquema HTTP se não fornecido
        if ollama_host and not ollama_host.startswith("http"):
            ollama_host = f"http://{ollama_host}"

        prompt = (
            "Você é o Gabriel, um analista de riscos corporativos sênior e agente de IA especialista da LexGrid em compliance e direito tributário brasileiro.\n"
            f"Gere um Parecer Executivo de Mitigação de Riscos de alta qualidade em formato Markdown para o CNPJ {cnpj}.\n\n"
            f"Dados de Risco da Empresa:\n"
            f"- Score Global de Risco: {scores['score_global']}/100 (onde 100 é o melhor cenário/saudável)\n"
            f"- Score Financeiro: {scores['score_financeiro']}/100\n"
            f"- Score Compliance/Tributário: {scores['score_compliance']}/100\n"
            f"- Score Cibernético: {scores['score_cibernetico']}/100\n"
            f"- Score Mercado: {scores['score_mercado']}/100\n"
            f"- Capital Social: R$ {capital_social:,.2f}\n\n"
            f"Pontos da Matriz SWOT da Empresa:\n"
            f"- Forças: {', '.join(swot['forcas'])}\n"
            f"- Fraquezas: {', '.join(swot['fraquezas'])}\n"
            f"- Oportunidades: {', '.join(swot['oportunidades'])}\n"
            f"- Ameaças: {', '.join(swot['ameacas'])}\n\n"
            "Diretrizes do Parecer:\n"
            "1. Escreva em Português do Brasil.\n"
            "2. Apresente um resumo claro do nível de risco atual da empresa.\n"
            "3. Indique recomendações de mitigação prioritárias para resolver as fraquezas (como passivos fiscais ou portas expostas no Shodan) e se defender das ameaças.\n"
            "4. Aponte como aproveitar as oportunidades tributárias listadas (como a Lei do Bem ou recuperação de TUST/TUSD) para injetar caixa na empresa.\n"
            "5. Limite a resposta a 3 ou 4 parágrafos no máximo, de forma muito direta, executiva e profissional. Não utilize placeholders. Escreva como um parecer oficial pronto para leitura da diretoria."
        )

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                response = await client.post(
                    f"{ollama_host}/api/generate",
                    json={
                        "model": "qwen3.6",
                        "prompt": prompt,
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    dados = response.json()
                    parecer = dados.get("response", "")
                    if parecer:
                        return parecer.strip()
        except Exception as e:
            # Silenciar logs na esteira local caso o Docker esteja offline
            pass

        # --- FALLBACK COGNITIVO ESTÁTICO (Caso Ollama esteja offline) ---
        return cls._generate_fallback_opinion(scores, swot, capital_social)

    @classmethod
    def _generate_fallback_opinion(
        cls,
        scores: Dict[str, float],
        swot: Dict[str, List[str]],
        capital_social: float
    ) -> str:
        """
        Gera um parecer estruturado dinâmico muito realista baseado na pontuação de risco.
        """
        score = scores["score_global"]
        
        # Define o diagnóstico geral
        if score >= 70:
            status_geral = "SAUDÁVEL (Risco Controlado)"
            conclusao = (
                "A empresa apresenta uma estrutura sólida de governança corporativa e conformidade fiscal. "
                "Com um score global de risco saudável, as defesas regulatórias estão ativas. A principal recomendação "
                "neste cenário é focar no aproveitamento das oportunidades financeiras identificadas para otimização de caixa."
            )
        elif score >= 40:
            status_geral = "ATENÇÃO (Risco Moderado)"
            conclusao = (
                "A empresa encontra-se em um patamar de risco moderado. Há vulnerabilidades administrativas ou "
                "operacionais que requerem planejamento de curto prazo para mitigação. A combinação de passivos judiciais ou "
                "exposição cibernética com pressões do mercado de crédito exige atenção da diretoria executiva."
            )
        else:
            status_geral = "CRÍTICO (Exige Auditoria Imediata)"
            conclusao = (
                "Cenário de risco crítico e severo. A concomitância de débitos ativos junto à PGFN, litígios "
                "judiciais ativos e portas vulneráveis abertas em sua infraestrutura de tecnologia impõe a necessidade de um "
                "plano emergencial de contingência. Recomenda-se auditoria jurídica e auditoria de sistemas de forma imediata."
            )

        # Montagem das recomendações baseada nos elementos da SWOT
        recom_list = []
        if swot["fraquezas"]:
            # Pega as primeiras 2 fraquezas
            for f in swot["fraquezas"][:2]:
                if "Dívida Ativa" in f or "PGFN" in f:
                    recom_list.append("Efetuar a renegociação ou adesão aos programas de transação tributária da PGFN para regularizar os débitos ativos e obter a CND.")
                elif "portas" in f or "Shodan" in f or "Cibernético" in f:
                    recom_list.append("Acionar a equipe de TI para fechamento das portas administrativas expostas (como RDP/PostgreSQL) e implementar whitelisting/VPN.")
                elif "Litígios" in f or "processo" in f:
                    recom_list.append("Provisionar garantias judiciais líquidas e traçar estratégias de acordo para encerrar os litígios cíveis/trabalhistas.")
                elif "protesto" in f.lower() or "títulos protestados" in f.lower():
                    recom_list.append("Providenciar a quitação imediata dos títulos junto ao credor e solicitar a baixa do protesto no cartório emissor, ou obter certidão positiva com efeito de negativa para resguardar o rating de crédito.")
                else:
                    recom_list.append(f"Adoção de controle preventivo para mitigar: {f.lower()}")

        if not recom_list:
            recom_list.append("Implementar auditoria semestral preditiva de regularidade cadastral e certidões.")

        # Oportunidades
        oport_text = ""
        if swot["oportunidades"]:
            oportunidades_validas = [o for o in swot["oportunidades"] if "revisão" not in o.lower()]
            if oportunidades_validas:
                oport_text = (
                    f"No âmbito tributário, identifica-se oportunidade de alta relevância estratégica voltada para **{oportunidades_validas[0]}**. "
                    "A implementação imediata deste planejamento contábil pode restabelecer margens e gerar compensações retroativas seguras."
                )

        # Montagem do Parecer Executivo em Markdown
        parecer = (
            f"### PARECER EXECUTIVO DE ANÁLISE DE RISCOS E MITIGAÇÃO\n\n"
            f"**Diagnóstico de Risco Geral:** A empresa está classificada sob o status de **{status_geral}** com pontuação ponderada de **{score}/100**.\n\n"
            f"{conclusao}\n\n"
            f"**Plano de Mitigação Sugerido:**\n"
            f"1. **Segurança de Sistemas e Compliance**: {recom_list[0]}\n"
        )
        
        if len(recom_list) > 1:
            parecer += f"2. **Ação Corretiva Tributária**: {recom_list[1]}\n"
            
        parecer += (
            f"3. **Proteção de Caixa**: Monitorar a exposição de crédito contra o cenário de taxa Selic a 10.5% e a transição da Reforma Tributária.\n\n"
            f"**Aproveitamento de Oportunidades:** {oport_text if oport_text else 'Recomenda-se auditoria preventiva de CNAEs secundários buscando créditos monofásicos.'}"
        )

        return parecer
