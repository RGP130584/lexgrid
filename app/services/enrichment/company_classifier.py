from app.models.entities.company_profile import CompanyProfile

class CompanyClassifier:
    SEGMENTS = {
        "agro": ["01", "02", "03"],
        "industria": ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33"],
        "energia": ["35"],
        "construcao": ["41", "42", "43"],
        "varejo": ["45", "46", "47", "48"],
        "logistica": ["49", "50", "51", "52", "53"],
        "tecnologia": ["61", "62", "63"],
        "saude": ["86", "87"],
        "servicos": ["69", "70", "71", "72", "73", "74", "77", "78", "79", "80", "81", "82", "94", "95", "96"]
    }

    @classmethod
    def classify_segment(cls, profile: CompanyProfile) -> str:
        main_prefix = profile.main_cnae.codigo[:2]
        
        for segment, prefixes in cls.SEGMENTS.items():
            if main_prefix in prefixes:
                return segment
                
        for cnae in profile.secondary_cnaes:
            prefix = cnae.codigo[:2]
            for segment, prefixes in cls.SEGMENTS.items():
                if prefix in prefixes:
                    return f"Misto (Pendente: {segment})"
        return "Geral/Outros"