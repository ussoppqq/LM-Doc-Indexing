from fastapi import APIRouter
from app.services.vector_store import search_vector
from app.services.llm_client import ask_llm

router = APIRouter()

@router.post("/")
def ask_question(question: str):
    context = search_vector(question)
    answer = ask_llm(question, context)

    return {
        "question": question,
        "answer": answer
    }
