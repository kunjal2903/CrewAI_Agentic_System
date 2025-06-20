from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def  __init__(self ,  model_name = "all-MiniLm-L6-v2"):
        self.model= SentenceTransformer(model_name)

    def embed_texts(self, texts:list[str])->list[list[float]]:
        return self.model.encode(texts , convert_to_tensor =False)
    