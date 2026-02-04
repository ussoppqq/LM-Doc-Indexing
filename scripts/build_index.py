import os
from app.services.document_loader import load_pdf
from app.services.text_splitter import split_text
from app.services.vector_store import build_index

UPLOAD_DIR = "data/uploads"

texts = []

for file in os.listdir(UPLOAD_DIR):
    if file.lower().endswith(".pdf"):
        text = load_pdf(os.path.join(UPLOAD_DIR, file))
        chunks = split_text(text)
        texts.extend(chunks)

build_index(texts)
print("Index built successfully")
