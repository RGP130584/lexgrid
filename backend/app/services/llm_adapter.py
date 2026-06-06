import os
import httpx
import json
from typing import Dict, Any, Union


async def execute_ai_tool(
    system_prompt: str,
    user_payload: str,
    require_json: bool = True
) -> Union[Dict[str, Any], str]:
    """
    Executa chamadas cognitivas de IA integrando com provedores em nuvem
    (Groq, OpenAI, etc.) via API compatível com o padrão OpenAI.
    """
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    model_name = os.getenv("LLM_MODEL", "llama3-70b-8192")

    if not api_key or "sua-chave" in api_key:
        raise ValueError(
            "LLM_API_KEY não configurada ou inválida no ambiente."
        )

    # Constrói o endpoint de chat completions
    url = f"{base_url.rstrip('/')}/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload}
        ],
        "temperature": 0.2
    }

    if require_json:
        payload["response_format"] = {"type": "json_object"}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            output = data["choices"][0]["message"]["content"]

            if require_json:
                return json.loads(output)
            return output
    except Exception as e:
        print(f"[LLM ADAPTER] Falha crítica na integração de IA: {e}")
        raise RuntimeError(
            f"Falha ao processar a ferramenta de IA: {e}"
        )

