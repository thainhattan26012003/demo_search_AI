from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# Initialize FastAPI
app = FastAPI(title="Embedding API")

model = SentenceTransformer('intfloat/multilingual-e5-large-instruct', trust_remote_code=True)

# Define the request body schema
class EmbedRequest(BaseModel):
    texts: list[str]


@app.post("/embed")
async def embed_text(request: EmbedRequest):
    embeddings = model.encode(request.texts).tolist()
    return {"embeddings": embeddings}
