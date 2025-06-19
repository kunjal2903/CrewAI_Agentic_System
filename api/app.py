from fastapi import FastAPI
from pydantic import BaseModel
from utils.embedding_utils import EmbeddingModel
from vectorstore.faiss_handler import FAISSHandler

app = FastAPI(title="News Search API")

embedder = EmbeddingModel()
vectorstore = FAISSHandler(dim=384) # Dimension of MiniLM embeddings


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/search")
def search_news(request: SearchRequest):
    if vectorstore.is_index_empty():
        return {
            "status": "error",
            "message": "FAISS index is empty. Run main.py to ingest news."
        }

    query_vector = embedder.embed_texts([request.query])
    results = vectorstore.search(query_vector, top_k=request.top_k)
    return {"results": results}
