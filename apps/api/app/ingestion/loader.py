from pathlib import Path
from pypdf import PdfReader
from app.ingestion.cleaner import clean_text

def load_pdf(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        cleaned_text = clean_text(raw_text)

        pages.append(
            {
                "page_number": page_number,
                "text": cleaned_text,
                "has_text": bool(cleaned_text),
            }
        )

    return pages
