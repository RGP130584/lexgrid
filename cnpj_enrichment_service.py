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

logger = get_logger("CNPJEnrichmentService")

class CNPJEnrichmentService:
    @classmethod
    async def analyze(cls, cnpj: str) -> CNPJResponse:
        cache_key = f"cnpj_enrichment:{cnpj}"
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
            qsa=raw_data.get("qsa", [])
        )
        
        segment = CompanyClassifier.classify_segment(profile)
        tax_profile = TaxProfile(**CnaeMapper.map_tax_profile(profile))
        domains, opportunities, flags = OpportunityContextBuilder.build_context(profile, segment)
        scores = ProfileScoring.calculate_scores(profile, segment, opportunities)
        
        response = CNPJResponse(
            cnpj=profile.cnpj, company_name=profile.company_name, trade_name=profile.trade_name,
            segment=segment, state=profile.state, city=profile.city, company_size=profile.company_size,
            main_cnae=profile.main_cnae, secondary_cnaes=profile.secondary_cnaes, tax_profile=tax_profile,
            eligible_domains=domains, potential_opportunities=opportunities, risk_flags=flags, scores=scores
        )
        cache_service.set(cache_key, response.model_dump())
        return response