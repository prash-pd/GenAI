import yaml
import requests
from qdrant_client import QdrantClient

OLLAMA_API_URL = "http://localhost:11434/api/generate"
EMBEDDING_API_URL = "http://localhost:11434/api/embeddings"     

def load_config():
    with open("config.yml") as f:
        return yaml.safe_load(f)    

def embed_query(query: str, model: str = "ollama/embedding-model") -> list:
    response = requests.post(
        EMBEDDING_API_URL,
        json={
            "model": model,
            "prompt": query
        }
    )
    response.raise_for_status()

    data = response.json()

    if "embedding" in data:
        return data["embedding"]

    if "embeddings" in data:
        embeddings = data["embeddings"]
        return embeddings[0] if embeddings and isinstance(embeddings[0], list) else embeddings

    raise Exception(f"No embeddings found in Ollama response. Keys returned: {list(data)}")




def ask_llm(context, question, model):

    prompt = f"""

    You are a HR assistant. 

    Use the provided context to answer the question. If the answer is not present in the context, respond with "I don't know".

    Context: {context}
    Question: {question}

    Please provide a concise and accurate answer based on the context.

    """

    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()

    data = response.json()

    if "response" not in data:
        raise Exception(f"No response found in Ollama output. Keys returned: {list(data)}")
    else:
        return data["response"]     



def main():
    config = load_config()

    # Connect to Qdrant
    client = QdrantClient(
        host=config["qdrant"]["host"],  
        port=config["qdrant"]["port"]       
    )

    # User question
    question = input("Enter your question: ")

    # Embed the question
    question_embedding = embed_query(question, config["ollama"]["embedding_model"]) 

    # Search for relevant chunks in Qdrant
    search_results = client.query_points(
        collection_name=config["qdrant"]["collection_name"],
        query=question_embedding,
        limit=3,
    ).points

    # Extract the context from the search results
    context = "\n".join([hit.payload["text"] for hit in search_results])    

    print("Context retrieved from Qdrant:")
    print(context)  

    #Ask the LLM with the context and question
    answer = ask_llm(context, question, config["ollama"]["llm_model"])
    print("Answer from LLM:")
    print(answer)

if __name__ == "__main__":
    main()


    


