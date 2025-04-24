import os
import requests
from dotenv import load_dotenv
from qdrant_client.http import models
from qdrant_client.models import PointStruct
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, FilterSelector
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, FilterSelector, PointStruct

load_dotenv(".env")

# Qdrant Client Setup
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# URL Vietnamese Embeddor (FastAPI)
EMBEDDING_API_URL = "http://embed_model_demo:8088/embed"

def embed(chunk):
    try:
        response = requests.post(EMBEDDING_API_URL, json={"texts": [chunk]})
        response.raise_for_status()  
        embeddings = response.json().get("embeddings", [])
        return embeddings[0] if embeddings else None
    except requests.exceptions.RequestException as e:
        print(f"? Error calling embedding API: {e}")
        return None

DEFAULT_DISTANCE = "COSINE"
    
class QdrantProvider:
    def __init__(self):
        # Initialize the QdrantProvider with a specific collection name
        test_embedidng = embed("test")
        self.vector_size = len(test_embedidng) if test_embedidng else 1024
        self.distance = DEFAULT_DISTANCE

    def create_collection(self, collection_name: str):
        # Check if the collection already exists
        if collection_name in self.list_collections():
            print(f"Collection `{collection_name}` already exists.")
            return

        # Create a new collection with the specified vector size and distance metric
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance[self.distance.upper()] if self.distance.upper() in models.Distance.__members__ else models.Distance.COSINE
            )
        )
        print(f"Collection created `{collection_name}`")
        
    def list_collections(self): 
        # List all existing collections in the Qdrant database
        collections = client.get_collections()
        return [col.name for col in collections.collections]
        
    def add_vectors_(self, collection_name, text, payload, id):
        """Add multiple vectors to the client collection."""
        points = []

        vector = embed(text)
        
        point = PointStruct(
            id=id,  
            vector=vector,  
            payload=payload
        )
        
        points.append(point)
        
        client.upsert(collection_name=collection_name, points=points)
        print(f"{len(points)} Vectors added to `{collection_name}`")

    def search_vector(self, collection_name: str, vector: list[float], limit=5, with_payload=True):
        # Perform the search query in client with the provided parameters
        search_result = client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,  # Limit the number of search results
            with_payload=with_payload,  # Whether to include payload in results
        )
        print(f"Vector searched `{collection_name}`")
        return search_result
    
    
    def delete_vectors(self, collection_name: str, vec_file_name: str):
        # Delete all vectors with the specified file_name from the collection
        filter = Filter(
            must=[FieldCondition(
                key="file_name",
                match=MatchValue(
                    value=vec_file_name
                )
            )]
        )
        client.delete(collection_name=collection_name, points_selector=FilterSelector(filter=filter))
        print(f"Vector deleted `{collection_name}`")