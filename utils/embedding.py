import requests
import os

OLLAMA_API_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/embeddings",
)

def generate_embeddings(chunks, model):
    embeddings = []

    for chunk in chunks:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": model, "prompt": chunk},
            timeout=120,
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to generate embedding. "
                f"Status code: {response.status_code}, Response: {response.text}"
            )

        embeddings.append(response.json()["embedding"])

    return embeddings