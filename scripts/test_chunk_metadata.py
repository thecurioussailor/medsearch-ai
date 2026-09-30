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
    print("=" * 120)

    for chunk in chunks:
        if "indicator_number" not in chunk:
            continue

        print(
            f"{chunk['chunk_id']} | "
            f"page={chunk['page_number']} | "
            f"type={chunk.get('section_type')} | "
            f"indicator={chunk['indicator_number']} | "
            f"{chunk['subdomain']} | "
            f"{chunk['indicator_name']}"
        )

    print("\nTAXONOMY CHUNKS")
    print("=" * 120)

    for chunk in chunks:
        if chunk.get("section_type") != "taxonomy":
            continue

        print(
            f"{chunk['chunk_id']} | "
            f"page={chunk['page_number']} | "
            f"type={chunk['section_type']}"
        )

    print("\nOTHER CHUNKS")
    print("=" * 120)

    for chunk in chunks:
        if chunk.get("section_type") != "other":
            continue

        print(
            f"{chunk['chunk_id']} | "
            f"page={chunk['page_number']} | "
            f"type={chunk['section_type']}"
        )


if __name__ == "__main__":
    main()