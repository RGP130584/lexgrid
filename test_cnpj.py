from fastapi.testclient import TestClient
from app.main import app
from app.utils.validators import validate_cnpj

client = TestClient(app)

def test_validate_cnpj():
    assert validate_cnpj("00000000000000") is False
    assert validate_cnpj("00.000.000/0001-91") is True

def test_analyze_invalid_cnpj():
    response = client.post("/api/v1/cnpj/analyze", json={"cnpj": "123"})
    assert response.status_code == 422
    
    response2 = client.post("/api/v1/cnpj/analyze", json={"cnpj": "00000000000000"})
    assert response2.status_code == 422