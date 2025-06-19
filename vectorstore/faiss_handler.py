
import faiss
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class FAISSHandler:
    def __init__(self, dim: int = 384, index_path="vectorstore/news.index", meta_path="vectorstore/meta.pkl"):
        
        self.index_path = index_path
        self.meta_path = meta_path
        self.dim = dim
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            print("🆕 Starting fresh FAISS index...")

    def is_index_empty(self) -> bool:
        return self.index.ntotal == 0

    def add_texts(self, vectors: list, metadatas: list):
        self.index.add(vectors)
        self.metadata.extend(metadatas)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query_vector, top_k=5):
        if self.is_index_empty():
            return [{"error": "FAISS index is empty. Please run ingestion first."}]
        D, I = self.index.search(query_vector, top_k)
        return [self.metadata[i] for i in I[0]]




       