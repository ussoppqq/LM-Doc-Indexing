from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed_texts(texts):
    return model.encode(texts)
