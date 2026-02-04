import requests
from app.config.settings import LM_STUDIO_BASE_URL

def ask_llm(question, context):
    payload = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": "Answer based on provided context"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    }

    response = requests.post(
        f"{LM_STUDIO_BASE_URL}/chat/completions",
        json=payload
    )

    return response.json()["choices"][0]["message"]["content"]
