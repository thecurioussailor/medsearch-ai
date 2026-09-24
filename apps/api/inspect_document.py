from app.ingestion.loader import load_pdf

pdf_path = "../../data/raw/diabetes_monitoring_guidance.pdf"

pages = load_pdf(pdf_path)

text_pages = [page for page in pages if page["has_text"]]
empty_pages = [page for page in pages if not page["has_text"]]

print(f"Total pages: {len(pages)}")
print(f"Pages with text: {len(text_pages)}")
print(f"Empty pages: {len(empty_pages)}")

print("\nEmpty pages:")

for page in empty_pages:
    print(f"- Page {page['page_number']}")

print("\nPage sizes:")

for page in pages:
    print(
        f"Page {page['page_number']:>2}: "
        f"{len(page['text']):>5} characters"
    )