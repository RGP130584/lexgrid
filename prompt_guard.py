import re
from typing import Tuple

class PromptGuard:
    """Defesa ativa contra Prompt Injection e Jailbreaks."""
    
    # Assinaturas conhecidas de ataques (DAN, Roleplay, Bypass)
    BLACKLIST_PATTERNS = [
        r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions",
        r"(?i)system\s+prompt",
        r"(?i)you\s+are\s+(now\s+)?(a\s+)?(developer|admin|root)",
        r"(?i)bypass\s+rules",
        r"(?i)forget\s+(your\s+)?rules",
        r"(?i)execute\s+command",
        r"(?i)print\s+(your\s+)?initial\s+prompt"
    ]

    JAILBREAK_KEYWORDS = {"dan", "do anything now", "developer mode", "god mode", "sudo"}

    @classmethod
    def analyze(cls, prompt: str) -> Tuple[bool, str]:
        """
        Analisa o prompt em busca de injeções.
        Retorna (is_safe, reason).
        """
        # 1. Regex Pattern Matching
        for pattern in cls.BLACKLIST_PATTERNS:
            if re.search(pattern, prompt):
                return False, f"Padrão de injeção detectado: {pattern}"
        
        # 2. Keyword Heuristics
        prompt_lower = prompt.lower()
        for kw in cls.JAILBREAK_KEYWORDS:
            if kw in prompt_lower:
                return False, f"Tentativa de Jailbreak detectada via keyword: {kw}"
                
        # 3. Escaping/Special Chars detection (simplificado)
        return True, "Prompt seguro."