from app.models.entities.company_profile import CompanyProfile

class ProfileScoring:
    @staticmethod
    def calculate_scores(profile: CompanyProfile, segment: str, ops: list) -> dict:
        scores = {
            "tributario": "LOW",
            "inovacao": "LOW",
            "maturidade": "LOW"
        }
        
        if profile.capital_social > 1000000:
            scores["maturidade"] = "HIGH"
        elif profile.capital_social > 100000:
            scores["maturidade"] = "MEDIUM"
            
        if "tust_tusd" in ops or "recuperacao_pis_cofins_monofasico" in ops:
            scores["tributario"] = "HIGH" if profile.capital_social < 5000000 else "CRITICAL"
        if "lei_do_bem" in ops:
            scores["inovacao"] = "HIGH"
        return scores