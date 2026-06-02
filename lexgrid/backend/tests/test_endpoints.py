#!/usr/bin/env python3
"""Test if the endpoints are properly registered"""

from main import app
from fastapi.testclient import TestClient
import json

print("=== App Routes ===")
for route in app.routes:
    print(f"Path: {route.path}, Methods: {getattr(route, 'methods', 'N/A')}")

client = TestClient(app)

print("\n=== Testing /health ===")
response = client.get("/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)[:500]}")

print("\n=== Testing /mcp/tools ===")
response2 = client.get("/mcp/tools")
print(f"Status: {response2.status_code}")
print(f"Response: {json.dumps(response2.json(), indent=2)[:500]}")

print("\n=== Testing /mcp/tools/call ===")
response3 = client.post("/mcp/tools/call", json={"tool_name": "consultar_sped_historico", "parameters": {"filename": "test.txt"}})
print(f"Status: {response3.status_code}")
print(f"Response: {json.dumps(response3.json(), indent=2)[:500]}")
