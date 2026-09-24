from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_text


pdf_path = "../../data/raw/diabetes_monitoring_guidance.pdf"

pages = load_pdf(pdf_path)

total_chunks = 0

for page in pages:
    if not page["has_text"]:
        continue

    chunks = chunk_text(page["text"])

    print(
        f"Page {page['page_number']:>2} "
        f"→ {len(chunks)} chunks"
    )

    total_chunks += len(chunks)

print()
print(f"Total chunks: {total_chunks}")