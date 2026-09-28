from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.bm25 import BM25Retriever


PDF_PATH = "data/raw/diabetes_monitoring_guidance.pdf"


def main():
    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages,
        document_id="who-diabetes-monitoring-2024",
    )

    retriever = BM25Retriever(chunks)

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

        results = retriever.retrieve(
            query,
            top_k=5,
        )

        for rank, result in enumerate(results, start=1):
            chunk = result["chunk"]

            print(
                f"{rank}. "
                f"score={result['score']:.4f} "
                f"page={chunk['page_number']}"
            )


if __name__ == "__main__":
    main()