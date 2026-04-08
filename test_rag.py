from src.ingestion.retrieval.rag_chain import build_rag_chain

rag = build_rag_chain()

question = "What safety precautions must be followed before operating ETF90?"

result = rag(question)

print("\nANSWER:\n", result["answer"])

print("\nSOURCES:")
for doc in result["sources"]:
    print(
        f"- Page {doc.metadata.get('page')} | "
        f"Type: {doc.metadata.get('type')}"
    )