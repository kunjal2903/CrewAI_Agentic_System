import os
import faiss
import pickle
from typing import List, Dict, Union, Optional
from sentence_transformers import SentenceTransformer
import numpy as np


class FAISSHandler:
    def __init__(self, dim: Optional[int] = None, namespace: str = "default"):
        base_path = f"vectorstore/{namespace}"
        os.makedirs(base_path, exist_ok=True)

        self.index_path = f"{base_path}/index.faiss"
        self.meta_path = f"{base_path}/meta.pkl"

        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = dim or self.embedding_model.get_sentence_embedding_dimension()

        self.index = None
        self.metadata = []

        self._load_or_initialize()

    def _load_or_initialize(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            print(f"📦 Loading FAISS index and metadata from: {self.index_path}")
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            print(f"📦 Initializing new FAISS index at: {self.index_path}")
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = []

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def add_documents(self, docs: List[Dict[str, str]]):
        """docs: list of {'content': str, 'url': str or other metadata}"""
        texts = [doc["content"] for doc in docs]
        metadatas = [{"url": doc.get("url", "")} for doc in docs]

        vectors = self.embedding_model.encode(texts, show_progress_bar=True)
        self.index.add(np.array(vectors))
        self.metadata.extend(metadatas)
        self._save()
        print(f"✅ Added {len(texts)} documents to FAISS.")

    def add_texts(self, vectors: List[List[float]], metadatas: List[Dict[str, str]]):
        self.index.add(np.array(vectors))
        self.metadata.extend(metadatas)
        self._save()
        print(f"✅ Added {len(vectors)} vectors manually to FAISS.")

    def search(
        self,
        query: Optional[str] = None,
        query_vector: Optional[Union[List[float], np.ndarray]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Union[str, float]]]:
        if self.index is None or self.index.ntotal == 0:
            return [{"error": "❌ FAISS index is empty."}]

        if query:
            query_vector = self.embedding_model.encode([query])
        elif query_vector is not None:
            if isinstance(query_vector, list):
                query_vector = np.array([query_vector])
            elif isinstance(query_vector, np.ndarray) and query_vector.ndim == 1:
                query_vector = np.expand_dims(query_vector, axis=0)
        else:
            return [{"error": "❌ No query or query vector provided."}]

        D, I = self.index.search(query_vector, top_k)
        results = []
        for rank, idx in enumerate(I[0]):
            if idx < len(self.metadata):
                results.append({
                    "rank": rank + 1,
                    "url": self.metadata[idx].get("url", "N/A"),
                    "score": float(D[0][rank])
                })
        return results