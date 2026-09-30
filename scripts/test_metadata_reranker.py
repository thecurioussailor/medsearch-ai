import json

from app.embeddings.embedder import Embedder
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.metadata_reranker import MetadataReranker
from app.retrieval.retriever import Retriever
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks


PDF_PATH = "data/raw/diabetes_monitoring_guidance.pdf"


print("Loading document...")

pages = load_pdf(PDF_PATH)

chunks = create_chunks(
    pages=pages,
    document_id="diabetes",
)

print(f"Total chunks: {len(chunks)}")

print("Loading embedding model...")

embedder = Embedder()

print("Generating embeddings...")

vectors = embedder.embed_texts(
    [chunk["text"] for chunk in chunks]
)

dense = Retriever(embedder)

bm25 = BM25Retriever(chunks)

hybrid = HybridRetriever(
    dense_retriever=dense,
    bm25_retriever=bm25,
)

reranker = MetadataReranker()


query = (
    "What indicator assesses the existence "
    "of national guidelines for diabetes management?"
)

results = hybrid.retrieve(
    query=query,
    chunks=chunks,
    vectors=vectors,
    top_k=10,
)

reranked = reranker.rerank(
    query=query,
    results=results,
    top_k=5,
)


print("\n" + "=" * 80)
print("HYBRID")
print("=" * 80)

for rank, result in enumerate(results[:5], start=1):
    chunk = result["chunk"]

    print(
        f"{rank}. "
        f"page={chunk['page_number']} | "
        f"indicator={chunk.get('indicator_number')} | "
        f"score={result['score']:.5f}"
    )


print("\n" + "=" * 80)
print("METADATA RERANKED")
print("=" * 80)

for rank, result in enumerate(reranked, start=1):
    chunk = result["chunk"]

    print(
        f"{rank}. "
        f"page={chunk['page_number']} | "
        f"indicator={chunk.get('indicator_number')} | "
        f"metadata={result['metadata_score']} | "
        f"final={result['final_score']:.5f}"
    )