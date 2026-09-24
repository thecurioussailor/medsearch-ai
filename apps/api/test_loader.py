from app.ingestion.loader import load_pdf

pdf_path = "../../data/raw/diabetes_monitoring_guidance.pdf"

pages = load_pdf(pdf_path)

print(f"Total pages: {len(pages)}")

for page in pages[:5]:
    print("\n")
    print("=" * 80)
    print(f"PAGE {page['page_number']}")
    print(f"TEXT LENGTH: {len(page['text'])}")
    print("=" * 80)
    print(repr(page["text"][:1000]))