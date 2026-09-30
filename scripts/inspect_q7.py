from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks

PDF_PATH = "data/raw/diabetes_monitoring_guidance.pdf"


def main():
    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages=pages,
        document_id="diabetes",
    )

    target_pages = [6, 21, 32, 42, 49, 61, 67, 69]

    for chunk in chunks:
        if chunk["page_number"] not in target_pages:
            continue

        print("\n" + "=" * 100)
        print(
            f"PAGE {chunk['page_number']} | "
            f"CHUNK {chunk['chunk_id']} | "
            f"TYPE {chunk.get('section_type')} | "
            f"INDICATOR {chunk.get('indicator_number')}"
        )
        print("=" * 100)

        print(chunk["text"])


if __name__ == "__main__":
    main()