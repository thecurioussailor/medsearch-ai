from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks


PDF_PATH = "data/raw/diabetes_monitoring_guidance.pdf"


def main():
    print("Loading document...")

    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages=pages,
        document_id="diabetes",
    )

    print(f"Total chunks: {len(chunks)}")

    print("\nINDICATOR CHUNKS")
    print("=" * 100)

    for chunk in chunks:
        if "indicator_number" not in chunk:
            continue

        print(
            f"{chunk['chunk_id']} | "
            f"page={chunk['page_number']} | "
            f"indicator={chunk['indicator_number']} | "
            f"{chunk['subdomain']} | "
            f"{chunk['indicator_name']}"
        )


if __name__ == "__main__":
    main()