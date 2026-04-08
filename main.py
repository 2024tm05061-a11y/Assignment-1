from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
import time

from src.ingestion.chunk_manager import get_all_chunks
from src.ingestion.retrieval.rag_chain import build_rag_chain


app = FastAPI(
    title="Multimodal RAG API",
    description="FastAPI-based Multimodal RAG System",
    version="1.0.0"
)

UPLOAD_DIR = "sample_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Build RAG chain once (loaded in memory)
rag_chain = None
CURRENT_PDF_PATH = None
start_time = time.time()


# --------------------
# HEALTH ENDPOINT
# --------------------
@app.get("/health")
def health():
    uptime = time.time() - start_time
    return {
        "status": "ok",
        "uptime_seconds": round(uptime, 2),
        "rag_loaded": True
    }


# --------------------
# INGEST ENDPOINT
# --------------------
@app.post("/ingest")
def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join("sample_documents", file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    global rag_chain, CURRENT_PDF_PATH
    CURRENT_PDF_PATH = file_path
    rag_chain = build_rag_chain(file_path)

    return {
        "message": "PDF ingested successfully",
        "filename": file.filename
    }



# --------------------
# QUERY ENDPOINT
# --------------------
class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_rag(request: QueryRequest):
    result = rag(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": [
            {
                "page": doc.metadata.get("page"),
                "type": doc.metadata.get("type")
            }
            for doc in result["sources"]
        ]
    }