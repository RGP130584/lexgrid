#!/usr/bin/env python3
"""Test if the endpoints are properly registered"""

from backend.main import app
import json

print("=== App Routes ===")
for route in app.routes:
    print(f"Path: {route.path}, Methods: {getattr(route, 'methods', 'N/A')}")

print("\n=== Testing /api/models ===")
from fastapi.testclient import TestClient
client = TestClient(app)

response = client.get("/api/models")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)[:500]}")

response2 = client.post("/api/generate", json={"prompt": "test", "model": "qwen2.5-coder:7b"})
print(f"\n=== Testing /api/generate ===")
print(f"Status: {response2.status_code}")
print(f"Response: {json.dumps(response2.json(), indent=2)[:500]}")
