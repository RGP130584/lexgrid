from app.models.entities.company_profile import CompanyProfile

class OpportunityContextBuilder:
    @staticmethod
    def build_context(profile: CompanyProfile, segment: str):
        eligible_domains = []
        potential_opportunities = []
        risk_flags = []
        
        all_cnaes = [profile.main_cnae.codigo] + [c.codigo for c in profile.secondary_cnaes]
        
        if segment in ["agro", "industria", "energia", "tecnologia"]:
            eligible_domains.append(segment)
            
        if any(c.startswith("62") or c.startswith("63") or c.startswith("20") for c in all_cnaes):
            eligible_domains.append("pd&i")
            potential_opportunities.append("lei_do_bem")
            
        if any(c[:2] in ["47", "56"] for c in all_cnaes):
            potential_opportunities.append("recuperacao_pis_cofins_monofasico")
            
        if any(c[:2] in ["28", "29", "30", "25", "10", "86"] for c in all_cnaes):
            potential_opportunities.append("tust_tusd")
            
        if profile.capital_social >= 500000.0:
            potential_opportunities.append("limitacao_base_terceiros_sistema_s")
            
        if profile.situacao_cadastral != "ATIVA" and profile.situacao_cadastral:
            risk_flags.append("empresa_inativa_ou_irregular")
            
        return eligible_domains, potential_opportunities, risk_flags