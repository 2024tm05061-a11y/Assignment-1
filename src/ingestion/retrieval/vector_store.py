import os
import json
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document


CHUNK_DIR = "data/chunks"
VECTOR_DB_DIR = "data/vector_store"


def load_latest_chunks():
    """
    Load the most recent chunk JSON file
    """
    files = sorted(
        [f for f in os.listdir(CHUNK_DIR) if f.endswith(".json")],
        reverse=True
    )

    if not files:
        raise FileNotFoundError("No chunk files found")

    latest_file = os.path.join(CHUNK_DIR, files[0])

    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)


def build_faiss_index():
    """
    Create FAISS vector store from chunks
    """
    chunks = load_latest_chunks()

    documents = [
        Document(
            page_content=chunk["content"],
            metadata={
                "type": chunk["type"],
                "page": chunk["page"],
                "source": chunk["source"],
            }
        )
        for chunk in chunks
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)

    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    vectorstore.save_local(VECTOR_DB_DIR)

    print("✅ FAISS vector store created and saved")

    return vectorstore