import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.ingestion.loader import load_pdf


PDF_PATH = REPO_ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"


def main():
    pages = load_pdf(PDF_PATH)

    for page in pages:
        if page["page_number"] in [32, 33, 34, 35]:
            print("\n" + "=" * 80)
            print(f"PAGE {page['page_number']}")
            print("=" * 80)
            print(page["text"])


if __name__ == "__main__":
    main()