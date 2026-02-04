import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_DIR = "data/index"
FAISS_PATH = os.path.join(INDEX_DIR, "index.faiss")
DOCS_PATH = os.path.join(INDEX_DIR, "docs.pkl")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def build_index(text_chunks: list[str]):
    os.makedirs(INDEX_DIR, exist_ok=True)

    embeddings = model.encode(text_chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, FAISS_PATH)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(text_chunks, f)


def load_index():
    index = faiss.read_index(FAISS_PATH)
    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)
    return index, documents


def search(index, documents, query, k=3):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k)
    return [documents[i] for i in indices[0]]
