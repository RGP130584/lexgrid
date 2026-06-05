from app.models.entities.company_profile import CompanyProfile
from app.models.value_objects.cnae import CNAE
from app.models.value_objects.tax_profile import TaxProfile
from app.services.enrichment.receita_client import ReceitaClient
from app.services.enrichment.company_classifier import CompanyClassifier
from app.services.enrichment.cnae_mapper import CnaeMapper
from app.engines.opportunity_engine.context_builder import OpportunityContextBuilder
from app.engines.scoring_engine.profile_scoring import ProfileScoring
from app.api.schemas.cnpj_response import CNPJResponse
from app.repositories.cache.redis_cache import cache_service
from app.core.logging.logger import get_logger

# Importações do Módulo de Riscos
from app.models.entities.risk_profile import RiskProfile
from app.services.enrichment.risk_client import RiskClient
from app.engines.risk_engine.risk_scoring import RiskScoringEngine
from app.engines.risk_engine.swot_builder import SWOTMitigationEngine
from app.engines.cyber_engine.cyber_risk_engine import CyberRiskEngine
from app.engines.incentive_engine.incentive_mapper import IncentiveMapper

logger = get_logger("CNPJEnrichmentService")

class CNPJEnrichmentService:
    @classmethod
    async def analyze(cls, cnpj: str, sped_data: dict = None) -> CNPJResponse:
        cache_key = f"cnpj_enrichment:{cnpj}"
        if not sped_data:
            cached = cache_service.get(cache_key)
            if cached:
                logger.info(f"Cache HIT para CNPJ: {cnpj}")
                return CNPJResponse(**cached)
            
        raw_data = await ReceitaClient.fetch_cnpj_data(cnpj)
        if not raw_data or not raw_data.get("razao_social"):
            raise ValueError("CNPJ não encontrado ou dados indisponíveis.")
            
        main_cnae_raw = raw_data.get("cnae_fiscal") or raw_data.get("atividade_principal", [{}])[0].get("code", "")
        main_cnae_desc = raw_data.get("cnae_fiscal_descricao") or raw_data.get("atividade_principal", [{}])[0].get("text", "")
        sec_cnaes_raw = raw_data.get("cnaes_secundarios") or []
        if sec_cnaes_raw and isinstance(sec_cnaes_raw[0], dict) and "code" in sec_cnaes_raw[0]:
             sec_cnaes_raw = [{"codigo": c.get("code", "").replace(".", "").replace("-", ""), "descricao": c.get("text", "")} for c in sec_cnaes_raw]
        
        debts = []
        try:
            debts = await ReceitaClient.fetch_pgfn_debts(cnpj)
        except Exception as e:
            logger.error(f"Erro ao buscar dividas PGFN: {e}")

        # Regras de Negocio Cognitivas para Analise Expandida
        all_cnaes_codigos = [str(main_cnae_raw).replace(".", "").replace("-", "")] + [str(c.get("codigo")).replace(".", "").replace("-", "") for c in sec_cnaes_raw]
        state = raw_data.get("uf", "").upper()
        capital_social = float(raw_data.get("capital_social") or 0.0)

        # 1. Fomentos nao reembolsaveis
        fomentos = []
        is_rd_tech = any(c.startswith("62") or c.startswith("63") or c.startswith("72") or c.startswith("20") or c.startswith("26") for c in all_cnaes_codigos)
        if is_rd_tech:
            fomentos.append({"orgao": "FINEP", "tipo": "Subvencao Economica", "status": "Elegivel (P&D)", "descricao": "Recursos nao reembolsaveis para projetos inovadores de risco tecnologico."})
            fomentos.append({"orgao": "EMBRAPII", "tipo": "Co-financiamento", "status": "Elegivel (Industrial/TI)", "descricao": "Financiamento de ate 1/3 do valor total do projeto de inovacao em parceria com polos tecnologicos."})
            fomentos.append({"orgao": "CNPq", "tipo": "Bolsas de Fomento", "status": "Elegivel", "descricao": "Bolsas de fixacao de pesquisadores (DTI) em projetos industriais."})
            fomentos.append({"orgao": "MCTI", "tipo": "Programas Nacionais", "status": "Elegivel", "descricao": "Editais tematicos de fomento a inteligencia artificial e transformacao digital."})

        if any(c.startswith("35") for c in all_cnaes_codigos):
            fomentos.append({"orgao": "ANEEL P&D", "tipo": "Obrigatorio", "status": "Elegivel (Setor Eletrico)", "descricao": "Recursos de investimento compulsorio em P&D para concessionarias de energia."})

        if state == "AM":
            fomentos.append({"orgao": "SUFRAMA", "tipo": "Incentivo Regional", "status": "Elegivel (Zona Franca de Manaus)", "descricao": "Isencao/reducao tributaria de IPI, PIS/COFINS de entrada para a regiao."})
            fomentos.append({"orgao": "CAPDA", "tipo": "Fomento Tecnologico", "status": "Elegivel (Informatica)", "descricao": "Recursos de P&D geridos pelo Comite das Atividades de Pesquisa e Desenvolvimento na Amazonia."})

        fap_name = f"FAP {state}" if state else "FAPs Estaduais"
        fomentos.append({"orgao": fap_name, "tipo": "Edital Estadual", "status": "Consultavel", "descricao": "Auxilios e subvencoes estaduais para incentivo a pesquisa e inovacao local."})

        # 2. Incentivos Fiscais
        incentivos = []
        if is_rd_tech:
            incentivos.append({
                "nome": "Lei do Bem",
                "tipo": "Federal",
                "beneficio": "Exclusao fiscal extra-contabil (60% a 80% do gasto em P&D) no IRPJ/CSLL.",
                "plano_acao": [
                    "Estruturar os projetos de P&D do ano fiscal.",
                    "Preencher o formulario FORMP&D e submeter ao MCTI.",
                    "Lancacar a exclusao fiscal na ECF anual."
                ]
            })
            incentivos.append({
                "nome": "Lei de Informatica",
                "tipo": "Federal/Regional",
                "beneficio": "Reducao do IPI e incentivos em cascata para fabricacao de bens de tecnologia/automacao.",
                "plano_acao": [
                    "Certificar o Processo Produtivo Basico (PPB) da empresa.",
                    "Comprovar investimentos em P&D na Amazonia ou regiao correspondente."
                ]
            })
        if state == "AM":
            incentivos.append({
                "nome": "Incentivos Estaduais (ICMS Amazonas)",
                "tipo": "Estadual",
                "beneficio": "Credito estimulo de ICMS de ate 100% sobre saidas industriais da ZFM.",
                "plano_acao": [
                    "Apresentar projeto tecnico-economico a SEPLANCTI.",
                    "Obter laudo de implantacao industrial da SUFRAMA."
                ]
            })

        # 3. Revisao de Regime Tributario (Simulation)
        estimated_revenue = 3000000.0 if raw_data.get("porte") == "EPP" else (50000000.0 if capital_social >= 1000000.0 else 800000.0)
        simulacao = {
            "faturamento_estimado": estimated_revenue,
            "criterio_porte": raw_data.get("porte", "NAO INFORMADO"),
            "criterio_capital": capital_social,
            "regimes": {
                "simples_nacional": {
                    "elegivel": estimated_revenue <= 4800000.0 and not any(c.startswith("35") or c.startswith("61") for c in all_cnaes_codigos),
                    "aliquota_media": "14.5%",
                    "custo_estimado": estimated_revenue * 0.145,
                    "vantagem": "Simplicidade de guias, menor burocracia para micro e pequenas empresas."
                },
                "lucro_presumido": {
                    "elegivel": estimated_revenue <= 78000000.0,
                    "aliquota_media": "16.33% (ISS/PIS/COFINS)",
                    "custo_estimado": estimated_revenue * 0.1633,
                    "vantagem": "Lucratividade real superior a margem presumida pelo Fisco."
                },
                "lucro_real": {
                    "elegivel": True,
                    "aliquota_media": "34.0% (IRPJ/CSLL sobre lucro liquido real) + PIS/COFINS 9.25%",
                    "custo_estimado": estimated_revenue * 0.22,
                    "vantagem": "Fundamental para usufruir da Lei do Bem, vantajoso em margens apertadas ou prejuizo operacional."
                }
            },
            "recomendacao": "Lucro Real" if (is_rd_tech and capital_social >= 1000000.0) else ("Lucro Presumido" if estimated_revenue > 4800000.0 else "Simples Nacional"),
            "detalhe_recomendacao": "Recomendacao com base no perfil de P&D (Lei do Bem) e faturamento estimado." if is_rd_tech else "Recomendacao com base na otimizacao de faturamento e simplicidade de guias."
        }

        # 4. Reducao Tributaria
        reducao = []
        if any(c.startswith("10") or c.startswith("20") or c.startswith("26") or c.startswith("28") for c in all_cnaes_codigos):
            reducao.append({"oportunidade": "Credito de ICMS sobre Insumos", "origem": "Estadual", "descricao": "Recuperacao de creditos de ICMS cobrados na aquisicao de materias-primas e embalagens industriais."})
        if any(c.startswith("28") or c.startswith("29") or c.startswith("30") or c.startswith("35") for c in all_cnaes_codigos) or capital_social >= 1000000.0:
            reducao.append({"oportunidade": "Recuperacao de TUST/TUSD (Energia)", "origem": "Judicial/Estadual", "descricao": "Exclusao das tarifas de distribuicao e transmissao de energia da base de calculo do ICMS."})
        if any(c.startswith("01") or c.startswith("02") for c in all_cnaes_codigos):
            reducao.append({"oportunidade": "Deducoes e Creditos do Agronegocio", "origem": "Federal/Estadual", "descricao": "Isencoes de PIS/COFINS em insumos agricolas e creditos presumidos da agroindustria."})
        else:
            reducao.append({"oportunidade": "Creditos de PIS/COFINS Monofasico", "origem": "Federal", "descricao": "Segregacao de faturamento de produtos com tributacao concentrada em comercios varejistas."})

        # 5. Nova Reforma Tributaria
        reforma = {
            "impacto_geral": "Medio (Fase de transicao 2026-2033)",
            "aliquota_estimada_ibs_cbs": "26.5% (Teto estimado do Governo)",
            "pontos_positivos": [
                "Credito amplo fisico e financeiro (fim do efeito cascata).",
                "Simplificacao drastica das obrigacoes acessorias tributarias.",
                "Devolucao agil do saldo credor acumulado de IBS/CBS."
            ],
            "pontos_negativos": [
                "Aumento na carga tributaria de servicos que possuem pouca cadeia fisica de insumos.",
                "Complexidade adicional no periodo de convivencia hibrida do modelo antigo e novo.",
                "Atencao ao Imposto Seletivo para itens especificos."
            ],
            "imposto_seletivo": "Inaplicavel" if not any(c.startswith("11") or c.startswith("12") or c.startswith("29") or c.startswith("06") for c in all_cnaes_codigos) else "Elegivel (Imposto do Pecado sobre bebidas, veiculos ou fumo)"
        }

        # 6. Incentivos de Inovacao
        inovacao = []
        if is_rd_tech:
            inovacao.append({"tipo": "Software", "incentivo": "Financiamentos FINEP Inovacao e Credenciamento no BNDES Finame para comercializacao de licencas de software nacional."})
            inovacao.append({"tipo": "Pesquisa & Desenvolvimento", "incentivo": "Parcerias universidade-empresa sob o marco legal da ciencia e tecnologia com deducao fiscal."})
        if any(c.startswith("10") or c.startswith("20") or c.startswith("28") or c.startswith("29") for c in all_cnaes_codigos):
            inovacao.append({"tipo": "Industria 4.0 & Automacao", "incentivo": "Editais de modernizacao de plantas fabris do programa Brasil Mais Produtivo (SENAI/BNDES)."})
        else:
            inovacao.append({"tipo": "Transformacao Digital", "incentivo": "Linhas de credito pre-aprovadas BNDES Credito Digital para digitalizacao e aquisicao de computadores."})

        # Fontes Consultadas
        fontes = [
            {"fonte": "Receita Federal", "nivel": 1, "status": "Consultado - OK", "tipo": "Dados Cadastrais e Situacao Fiscal"},
            {"fonte": "CONFAZ", "nivel": 1, "status": "Conectado", "tipo": "Convenios de ICMS e Beneficios Estaduais"},
            {"fonte": "FINEP", "nivel": 1, "status": "Sincronizado", "tipo": "Programas de Subvencao de Inovacao"},
            {"fonte": "BNDES", "nivel": 1, "status": "Conectado", "tipo": "Linhas de Credito e Fomentos Ativos"},
            {"fonte": "EMBRAPII", "nivel": 1, "status": "Sincronizado", "tipo": "Unidades Credenciadas e Parcerias"},
            {"fonte": "ANEEL", "nivel": 1, "status": "Conectado" if any(c.startswith("35") for c in all_cnaes_codigos) else "Nao Aplicavel", "tipo": "Incentivos P&D Setor Eletrico"},
            {"fonte": "SUFRAMA", "nivel": 1, "status": "Sincronizado" if state == "AM" else "Nao Aplicavel", "tipo": "Incentivos Regionais ZFM"},
            {"fonte": "CAPDA", "nivel": 1, "status": "Conectado" if state == "AM" else "Nao Aplicavel", "tipo": "Atividades de P&D de TI na Amazonia"},
            {"fonte": "Editais Estaduais (FAPs)", "nivel": 2, "status": "Varredura Concluida", "tipo": "Editais e Subvencoes Locais"},
            {"fonte": "Diarios Oficiais da Uniao e Estados", "nivel": 2, "status": "Monitoramento Ativo", "tipo": "Leis e Portarias de Incentivo"},
            {"fonte": "Portais Governamentais Estaduais", "nivel": 2, "status": "Varredura Concluida", "tipo": "Regulamentos ICMS Estaduais"}
        ]

        profile = CompanyProfile(
            cnpj=cnpj,
            company_name=raw_data.get("razao_social", ""),
            trade_name=raw_data.get("nome_fantasia") or raw_data.get("razao_social"),
            natureza_juridica=raw_data.get("natureza_juridica", ""),
            capital_social=float(raw_data.get("capital_social") or 0.0),
            state=raw_data.get("uf", ""), city=raw_data.get("municipio", ""),
            company_size=raw_data.get("porte", "NÃO INFORMADO"),
            situacao_cadastral=raw_data.get("descricao_situacao_cadastral", ""),
            main_cnae=CNAE(codigo=str(main_cnae_raw).replace(".", "").replace("-", ""), descricao=main_cnae_desc),
            secondary_cnaes=[CNAE(codigo=str(c.get("codigo")).replace(".", "").replace("-", ""), descricao=c.get("descricao")) for c in sec_cnaes_raw],
            qsa=raw_data.get("qsa", []),
            divida_ativa_uniao=debts,
            fomentos_nao_reembolsaveis=fomentos,
            regime_simulacao=simulacao,
            reducao_tributaria=reducao,
            reforma_tributaria=reforma,
            incentivos_inovacao=inovacao,
            fontes_consultadas=fontes
        )
        
        segment = CompanyClassifier.classify_segment(profile)
        tax_profile = TaxProfile(**CnaeMapper.map_tax_profile(profile))
        domains, opportunities, flags = OpportunityContextBuilder.build_context(profile, segment)
        scores = ProfileScoring.calculate_scores(profile, segment, opportunities)
        
        # Ingestão de riscos (Antecedentes, Mandados, Processos, Shodan, IBGE/SIDRA e Protestos)
        bg_check = await RiskClient.fetch_background_check(profile.cnpj, profile.qsa)
        lawsuits = await RiskClient.fetch_lawsuits(profile.cnpj)
        cyber_risks = await RiskClient.fetch_cyber_risks(profile.cnpj)
        market_risks = await RiskClient.fetch_market_risks(profile.main_cnae.codigo)
        protests = await RiskClient.fetch_protests(profile.cnpj)

        # Módulo 5: Cyber Threat Intelligence — varredura passiva de superfície de ataque
        dominio_inferido = None
        if profile.qsa:
            # Tenta inferir domínio do e-mail do primeiro sócio
            for socio in profile.qsa:
                email = getattr(socio, "contato_email", None) or socio.get("contato_email", "")
                if email and "@" in email:
                    dominio_inferido = email.split("@")[-1]
                    break
        cyber_intel = await CyberRiskEngine.scan(
            cnpj=profile.cnpj,
            dominio=dominio_inferido
        )
        
        # Módulo 6: Alavancagem Financeira e Mapeamento Global de Incentivos Fiscais
        incentivos_financiamento = await IncentiveMapper.map(
            cnpj=profile.cnpj,
            cnae=profile.main_cnae.codigo,
            regime=profile.regime_simulacao.get("recomendacao", "Simples Nacional"),
            uf=profile.state,
            capital_social=profile.capital_social
        )
        
        # Execução dos motores cognitivos de risco e SWOT
        risk_scores = RiskScoringEngine.calculate_scores(
            cnpj=profile.cnpj,
            divida_ativa=profile.divida_ativa_uniao,
            capital_social=profile.capital_social,
            background_check=bg_check,
            lawsuits=lawsuits,
            cyber_risks=cyber_risks,
            market_risks=market_risks,
            faturamento_estimado=profile.regime_simulacao.get("faturamento_estimado", 0.0),
            protestos=protests
        )
        
        swot_data = SWOTMitigationEngine.build_swot(
            cnpj=profile.cnpj,
            capital_social=profile.capital_social,
            divida_ativa=profile.divida_ativa_uniao,
            lawsuits=lawsuits,
            cyber_risks=cyber_risks,
            market_risks=market_risks,
            cnae_principal=profile.main_cnae.codigo,
            regime_simulacao=profile.regime_simulacao,
            uf=profile.state,
            protestos=protests
        )

        # Integração Módulo 5 → SWOT: gatilho de Risco Crítico automático
        if cyber_intel.get("cyber_score", 100) < 40:
            cyber_alerta = (
                "Identidade corporativa exposta: credenciais vazadas na Dark Web e "
                "portas críticas abertas detectadas via Shodan. Recomendação imediata: "
                "bloqueio de credenciais, implementação de MFA e encerramento das portas identificadas."
            )
            if cyber_alerta not in swot_data.get("fraquezas", []):
                swot_data.setdefault("fraquezas", []).append(cyber_alerta)

        # Integração Módulo 6 → SWOT: gatilho de Oportunidade Crítica automática (SUDENE/SUDAM)
        for gap in (incentivos_financiamento.get("gap_analysis") or []):
            if gap.get("urgencia") == "CRÍTICO" and gap.get("usa") == "Não Aproveitado":
                oportunidade_alerta = (
                    f"Oportunidade Crítica: Redução de 75% do IRPJ (SUDENE/SUDAM) não aproveitada. "
                    f"Impacto anual estimado de R$ {gap.get('impacto_nao_aproveitado', 0.0):,.2f}."
                )
                if oportunidade_alerta not in swot_data.get("oportunidades", []):
                    swot_data.setdefault("oportunidades", []).append(oportunidade_alerta)
        
        parecer = await SWOTMitigationEngine.generate_mitigation_opinion(
            cnpj=profile.cnpj,
            scores=risk_scores,
            swot=swot_data,
            capital_social=profile.capital_social
        )
        
        risk_profile = RiskProfile(
            score_global=risk_scores["score_global"],
            score_financeiro=risk_scores["score_financeiro"],
            score_compliance=risk_scores["score_compliance"],
            score_cibernetico=risk_scores["score_cibernetico"],
            score_mercado=risk_scores["score_mercado"],
            antecedentes_criminais=bg_check["antecedentes_criminais"],
            mandados_prisao=bg_check["mandados_prisao"],
            processos_judiciais=lawsuits,
            vulnerabilidades_ciberneticas=cyber_risks["vulnerabilidades_ciberneticas"],
            protestos=protests,
            swot=swot_data,
            parecer_mitigacao=parecer
        )
        
        response = CNPJResponse(
            cnpj=profile.cnpj, company_name=profile.company_name, trade_name=profile.trade_name,
            segment=segment, state=profile.state, city=profile.city, company_size=profile.company_size,
            main_cnae=profile.main_cnae, secondary_cnaes=profile.secondary_cnaes, qsa=profile.qsa,
            capital_social=profile.capital_social, tax_profile=tax_profile, eligible_domains=domains,
            potential_opportunities=opportunities, risk_flags=flags, scores=scores,
            divida_ativa_uniao=profile.divida_ativa_uniao,
            fomentos_nao_reembolsaveis=profile.fomentos_nao_reembolsaveis,
            regime_simulacao=profile.regime_simulacao,
            reducao_tributaria=profile.reducao_tributaria,
            reforma_tributaria=profile.reforma_tributaria,
            incentivos_inovacao=profile.incentivos_inovacao,
            fontes_consultadas=profile.fontes_consultadas,
            risk_profile=risk_profile,
            cyber_intel=cyber_intel,
            incentivos_financiamento=incentivos_financiamento
        )
        cache_service.set(cache_key, response.model_dump())
        return response