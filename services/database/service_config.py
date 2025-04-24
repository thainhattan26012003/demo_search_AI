from dotenv import load_dotenv
from .vector_db import QdrantProvider
load_dotenv(".env")


QDRANT_COLLECTION = "AI_Assistant"

vectordb_provider = QdrantProvider()
vectordb_provider.create_collection(QDRANT_COLLECTION)
