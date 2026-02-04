from app.services.vector_store import load_index, search
from app.services.llm_client import ask_llm

QUESTION = "Apa topik utama dari dokumen ini?"

# 1. load index
index, documents = load_index()

# 2. search context
contexts = search(index, documents, QUESTION, k=3)

context_text = "\n".join(contexts)

print("=== CONTEXT DARI DOKUMEN ===")
print(context_text)

# 3. ask LLM
answer = ask_llm(context_text, QUESTION)

print("\n=== JAWABAN LLM ===")
print(answer)
