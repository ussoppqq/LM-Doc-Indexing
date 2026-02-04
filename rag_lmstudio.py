import pickle
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

# ===============================
# CONFIG
# ===============================
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "local-model"  
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

INDEX_PATH = "data/index/index.faiss"
DOCS_PATH = "data/index/docs.pkl"

TOP_K = 3
TEMPERATURE = 0.2

# ===============================
# LOAD EMBEDDING MODEL
# ===============================
print("Loading embedding model...")
embedder = SentenceTransformer(EMBEDDING_MODEL)

# ===============================
# LOAD INDEX & DOCS
# ===============================
print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading documents...")
with open(DOCS_PATH, "rb") as f:
    documents = pickle.load(f)

# ===============================
# SEARCH FUNCTION
# ===============================
def retrieve_context(query, top_k=TOP_K):
    query_embedding = embedder.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    contexts = []
    for idx in indices[0]:
        if idx < len(documents):
            contexts.append(documents[idx])

    return "\n\n".join(contexts)

# ===============================
# ASK LM STUDIO
# ===============================
def ask_lmstudio(context, question):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten AI. "
                    "Jawablah HANYA berdasarkan konteks yang diberikan. "
                    "Jika jawaban tidak ada di konteks, katakan 'Informasi tidak ditemukan dalam dokumen.'"
                )
            },
            {
                "role": "user",
                "content": f"""
Konteks:
{context}

Pertanyaan:
{question}
"""
            }
        ],
        "temperature": TEMPERATURE
    }

    response = requests.post(LM_STUDIO_URL, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

# ===============================
# MAIN LOOP
# ===============================
if __name__ == "__main__":
    print("\n=== RAG LM Studio Ready ===\n")

    while True:
        question = input("Tanya (ketik 'exit' untuk keluar): ")
        if question.lower() == "exit":
            break

        context = retrieve_context(question)
        answer = ask_lmstudio(context, question)

        print("\n--- JAWABAN ---")
        print(answer)
        print("\n----------------\n")
