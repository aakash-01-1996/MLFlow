#!/usr/bin/env python
"""Test script to make predictions against the served model."""
import requests
import json

# Test the CustomModel endpoint
endpoint = "http://127.0.0.1:5001/invocations"
headers = {"Content-Type": "application/json"}

# Test data
data = {"inputs": ["hello", "world"]}

try:
    response = requests.post(endpoint, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.ConnectionError:
    print("❌ Connection failed. Make sure the model server is running:")
    print("   .venv/bin/mlflow models serve --model-uri 'models:/CustomModel/2' --port 5001 --no-conda")
