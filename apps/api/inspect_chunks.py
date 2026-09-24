from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_text

pdf_path = "../../data/raw/diabetes_monitoring_guidance.pdf"

pages = load_pdf(pdf_path)

def inspect_page(page_number: int):
    page = next(
        page for page in pages
        if page["page_number"] == page_number
    )

    chunks = chunk_text(page["text"])

    print("\n" + "=" * 100)
    print(f"PAGE {page_number} | {len(chunks)} CHUNKS")
    print("=" * 100)

    for index, chunk in enumerate(chunks, start=1):
        print("\n" + "-" * 100)
        print(f"CHUNK {index}")
        print(f"CHARACTERS: {len(chunk)}")
        print("-" * 100)
        print(chunk)


# Start with a few representative pages
for page_number in [5, 20, 32, 85, 90]:
    inspect_page(page_number)