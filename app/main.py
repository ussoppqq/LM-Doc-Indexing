from fastapi import FastAPI
from app.api import upload, query

app = FastAPI(title="LM Studio Doc Indexing")

app.include_router(upload.router, prefix="/upload")
app.include_router(query.router, prefix="/query")

@app.get("/")
def root():
    return {"status": "LM Studio Document Indexing API running"}
