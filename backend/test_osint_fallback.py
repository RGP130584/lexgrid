import asyncio
import httpx
import sys
import os
from unittest.mock import AsyncMock, patch

# Ajusta path para importar services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from osint_engine import call_mcp_tool_universal_master

async def simulate_fallback():
    print("\n" + "="*60)
    print("TESTE DE FALLBACK E CONCORRENCIA - OSINT MASTER v5.5.0")
    print("="*60)

    cnpj_teste = "00000000000000"

    # Mockando o comportamento do httpx.AsyncClient.get
    async def mock_get(url, **kwargs):
        mock_resp = AsyncMock()
        if "brasilapi" in str(url):
            # BrasilAPI falha (500 ou Timeout simulado)
            mock_resp.status_code = 500
        elif "receitaws" in str(url):
            # ReceitaWS responde com sucesso
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "status": "OK", "nome": "EMPRESA TESTE FALLBACK",
                "atividade_principal": [{"code": "62.01-5-00", "text": "Desenvolvimento de Software"}]
            }
        elif "pgfn" in str(url):
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"resultado": []}
        return mock_resp

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        print("[*] Iniciando busca master (BrasilAPI vs ReceitaWS)...")
        resultado = await call_mcp_tool_universal_master(cnpj_teste)
        
        if resultado.get("fonte") == "ReceitaWS":
            print("[OK] Fallback detectado com sucesso: BrasilAPI falhou e ReceitaWS assumiu.")
            print(f"     Razão Social: {resultado.get('razao_social')}")
            return True
        else:
            print("[ERRO] Fallback não funcionou ou fonte inesperada.")
            return False

if __name__ == "__main__":
    asyncio.run(simulate_fallback())