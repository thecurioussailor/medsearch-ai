import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.retriever import Retriever
from app.retrieval.query_expander import QueryExpander
from app.retrieval.multi_query import MultiQueryRetriever


PDF_PATH = REPO_ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"


def main():
    print("Loading document...")

    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages,
        document_id="who-diabetes-monitoring-2024",
    )

    print(f"Total chunks: {len(chunks)}")

    embedder = Embedder()

    texts = [chunk["text"] for chunk in chunks]
    vectors = embedder.embed_texts(texts)

    dense_retriever = Retriever(embedder)

    expander = QueryExpander()

    retriever = MultiQueryRetriever(
        retriever=dense_retriever,
        query_expander=expander,
    )

    query = "What indicators measure diabetes service delivery?"

    print("\nOriginal query:")
    print(query)

    print("\nExpanded queries:")

    for expanded_query in expander.expand(query):
        print(f"- {expanded_query}")

    results = retriever.retrieve(
        query=query,
        chunks=chunks,
        vectors=vectors,
        top_k=10,
    )

    print("\n" + "=" * 80)
    print("MULTI-QUERY RESULTS")
    print("=" * 80)

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(
            f"{rank}. "
            f"score={result['score']:.4f} "
            f"page={chunk['page_number']} "
            f"chunk={chunk['chunk_id']}"
        )


if __name__ == "__main__":
    main()