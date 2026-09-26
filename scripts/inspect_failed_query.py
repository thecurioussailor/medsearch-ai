import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.retriever import Retriever


PDF_PATH = REPO_ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"


def main():
    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages,
        document_id="who-diabetes-monitoring-2024",
    )

    embedder = Embedder()
    retriever = Retriever(embedder)

    texts = [chunk["text"] for chunk in chunks]
    vectors = embedder.embed_texts(texts)

    query = "What indicators measure diabetes service delivery?"

    results = retriever.retrieve(
        query=query,
        chunks=chunks,
        vectors=vectors,
        top_k=5,
    )

    print("\nQUERY")
    print("=" * 80)
    print(query)

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print("\n" + "=" * 80)
        print(f"RANK {rank}")
        print(f"Score: {result['score']:.4f}")
        print(f"Page: {chunk['page_number']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print("-" * 80)
        print(chunk["text"])


if __name__ == "__main__":
    main()