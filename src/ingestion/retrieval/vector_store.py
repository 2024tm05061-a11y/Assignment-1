from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from src.ingestion.chunk_manager import get_all_chunks


def build_vector_store():
    """
    Embed all chunks and build FAISS vector store
    """
    chunks = get_all_chunks()

    documents = [
        Document(
            page_content=chunk["content"],
            metadata={
                "type": chunk["type"],
                "page": chunk["page"],
                "source": chunk["source"]
            }
        )
        for chunk in chunks
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(documents, embeddings)

    return vector_store
