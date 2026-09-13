from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType
import uuid

def setup_collection(client: QdrantClient, collection_name: str, vector_size: int):
    """
    Sets up a Qdrant collection with the specified name and vector size.
    
    Args:
        client (QdrantClient): The Qdrant client instance.
        collection_name (str): The name of the collection to create.
        vector_size (int): The size of the vectors to be stored in the collection.
    """
    # Define the vector parameters for the collection
    # vector_params = VectorParams(size=vector_size, distance=Distance.COSINE)
    
    # Create the collection with the specified parameters
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE    
        )
    )   


def ingest_chunks(
    client: QdrantClient,
    collection_name: str,
    chunks: list,
    embeddings: list,
):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk},
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    client.upsert(
        collection_name=collection_name,
        points=points,
    )