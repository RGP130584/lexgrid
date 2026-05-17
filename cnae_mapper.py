from app.models.entities.company_profile import CompanyProfile

class CnaeMapper:
    @staticmethod
    def map_tax_profile(profile: CompanyProfile) -> dict:
        is_simples = profile.company_size in ["MICRO EMPRESA", "EMPRESA DE PEQUENO PORTE", "MEI"]
        
        if profile.main_cnae.codigo.startswith("64"):
            is_simples = False
            
        return {
            "is_simples_nacional": is_simples,
            "presumed_profit_eligible": profile.capital_social < 78000000.0,
            "real_profit_eligible": True
        }