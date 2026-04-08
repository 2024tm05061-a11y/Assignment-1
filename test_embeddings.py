from src.retrieval.vector_store import build_faiss_index

vectorstore = build_faiss_index()

results = vectorstore.similarity_search(
    "operating safety instructions",
    k=3
)

for i, doc in enumerate(results, 1):
    print(f"\n--- RESULT {i} ---")
    print("Type:", doc.metadata["type"])
    print("Page:", doc.metadata["page"])
    print("Content preview:", doc.page_content[:200])