import yaml
from qdrant_client import QdrantClient    

from utils.loader import load_pdf
from utils.preprocessing import clean_text
from utils.chunking import chunk_text
from utils.embedding import generate_embeddings
from utils.vectorstore import setup_collection, ingest_chunks

import os

PDF_PATH = os.getenv("PDF_PATH", "hr_policy_detailed_5_pages.pdf")

print("Current directory:", os.getcwd())
print("Config exists:", os.path.exists("config.yml"))

def load_config():
    with open("config.yml") as f:
        return yaml.safe_load(f)

def main():

    config = load_config()

    print("Loading PDF...")
    text = load_pdf(PDF_PATH)
    
    print("Cleaning text...")
    cleaned_text = clean_text(text)
    
    print("Chunking text...")
    chunks = chunk_text(cleaned_text)

    print("Total chunks:", len(chunks))
    
    print("Generating embeddings...")
    print("Generating embeddings via Ollama...")
    embeddings = generate_embeddings(
        chunks,
        config["ollama"]["embedding_model"]
    )
    
    print("Connecting to Qdrant...")
    client = QdrantClient(
        host=os.getenv("QDRANT_HOST", config["qdrant"]["host"]),
        port=int(os.getenv("QDRANT_PORT", config["qdrant"]["port"]))
    )

    setup_collection(
        client,
        config["qdrant"]["collection_name"],
        config["qdrant"]["vector_size"]
    )

    print("Ingesting vectors...")
    ingest_chunks(
        client,
        config["qdrant"]["collection_name"],
        chunks,
        embeddings
    )

    print("✅ Ingestion completed")
    
if __name__ == "__main__":
    main()   

