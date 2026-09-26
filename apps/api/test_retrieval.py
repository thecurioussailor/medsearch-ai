from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.embeddings.embedder import Embedder


PDF_PATH = "../../data/raw/diabetes_monitoring_guidance.pdf"
DOCUMENT_ID = "who-diabetes-monitoring-2024"


# Load document
pages = load_pdf(PDF_PATH)

# Create chunks
chunks = create_chunks(
    pages,
    document_id=DOCUMENT_ID,
)

print(f"Total chunks: {len(chunks)}")


# Load embedding model
embedder = Embedder()

# Embed all chunks
texts = [chunk["text"] for chunk in chunks]

vectors = embedder.embed_texts(texts)

print(f"Total vectors: {len(vectors)}")
print(f"Vector dimensions: {len(vectors[0])}")


# User query
query = "What indicators are used to monitor diabetes?"

query_vector = embedder.embed_text(query)


# Calculate similarity
results = []

for chunk, vector in zip(chunks, vectors):

    score = sum(
        query_value * chunk_value
        for query_value, chunk_value in zip(query_vector, vector)
    )

    results.append(
        {
            "score": score,
            "chunk": chunk,
        }
    )


# Sort by similarity
results.sort(
    key=lambda result: result["score"],
    reverse=True,
)


# Display top 5
print("\n")
print("=" * 100)
print("TOP 5 RESULTS")
print("=" * 100)

for rank, result in enumerate(results[:5], start=1):

    chunk = result["chunk"]

    print("\n" + "-" * 100)
    print(f"RANK: {rank}")
    print(f"SCORE: {result['score']:.4f}")
    print(f"PAGE: {chunk['page_number']}")
    print(f"CHUNK ID: {chunk['chunk_id']}")
    print("-" * 100)

    print(chunk["text"][:500])