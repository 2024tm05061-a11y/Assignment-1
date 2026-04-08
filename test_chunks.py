from src.ingestion.chunk_manager import get_all_chunks

chunks = get_all_chunks()

print("✅ Total chunks:", len(chunks))

type_counts = {"text": 0, "table": 0, "image": 0}

for chunk in chunks:
    type_counts[chunk["type"]] += 1

print("✅ Chunk type counts:", type_counts)
