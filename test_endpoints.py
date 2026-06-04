#!/usr/bin/env python3
"""Test if the endpoints are properly registered"""

from backend.main import app
import json

print("=== App Routes ===")
for route in app.routes:
    print(f"Path: {route.path}, Methods: {getattr(route, 'methods', 'N/A')}")

print("\n=== Testing /health ===")
from fastapi.testclient import TestClient
client = TestClient(app)

response = client.get("/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

response2 = client.get("/api/v1/cnpj/00000000000191")
print(f"\n=== Testing /api/v1/cnpj/00000000000191 ===")
print(f"Status: {response2.status_code}")
try:
    print(f"Response: {json.dumps(response2.json(), indent=2)[:1000]}")
except Exception:
    print(f"Response Text: {response2.text[:1000]}")

