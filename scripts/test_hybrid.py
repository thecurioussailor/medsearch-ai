import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.retriever import Retriever
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever


PDF_PATH = REPO_ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"


def main():
    print("Loading document...")

    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages,
        document_id="who-diabetes-monitoring-2024",
    )

    print(f"Total chunks: {len(chunks)}")

    # -----------------------------
    # Dense retrieval
    # -----------------------------

    print("Loading embedding model...")

    embedder = Embedder()

    print("Generating embeddings...")

    texts = [chunk["text"] for chunk in chunks]
    vectors = embedder.embed_texts(texts)

    dense_retriever = Retriever(embedder)

    # -----------------------------
    # BM25 retrieval
    # -----------------------------

    print("Building BM25 index...")

    bm25_retriever = BM25Retriever(chunks)

    # -----------------------------
    # Hybrid retrieval
    # -----------------------------

    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        bm25_retriever=bm25_retriever,
    )

    queries = [
        "What are the risk factors for diabetes?",
        "What are the global diabetes coverage targets?",
        "How is diabetes prevalence monitored?",
        "What indicators measure diabetes service delivery?",
        "What indicators are used to monitor diabetes?",
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print(query)
        print("=" * 80)

        results = hybrid_retriever.retrieve(
            query=query,
            chunks=chunks,
            vectors=vectors,
            top_k=5,
        )

        for rank, result in enumerate(results, start=1):
            chunk = result["chunk"]

            print(
                f"{rank}. "
                f"RRF score={result['score']:.6f} "
                f"page={chunk['page_number']} "
                f"chunk={chunk['chunk_id']}"
            )


if __name__ == "__main__":
    main()