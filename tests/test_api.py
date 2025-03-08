import os
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, ".")  # Ensure current directory is in path
from app import app

# Disable rate limiting for testing
os.environ["DISABLE_RATE_LIMITING"] = "true"

client = TestClient(app)

def test_query():
    response = client.post("/query", json={"query": "Hello!"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_summarization():
    text = (
        "Artificial intelligence is transforming industries by automating tasks, "
        "improving efficiency, and enabling new capabilities. Companies are using AI "
        "to analyze data, optimize processes, and create innovative solutions in healthcare, "
        "finance, and transportation."
    )

    response = client.post("/summarize", json={"text": text})
    assert response.status_code == 200
    assert "summary" in response.json()
