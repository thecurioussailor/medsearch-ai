from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks


pdf_path = "../../data/raw/diabetes_monitoring_guidance.pdf"

document_id = "who-diabetes-monitoring-2024"

pages = load_pdf(pdf_path)

chunks = create_chunks(
    pages,
    document_id=document_id,
)

print(f"Total chunks: {len(chunks)}")

print("\nFirst chunk:")
print("-" * 80)
print(chunks[0])

print("\nLast chunk:")
print("-" * 80)
print(chunks[-1])