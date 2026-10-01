import sys
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

load_dotenv(REPO_ROOT / "apps" / "api" / ".env")


from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.taxonomy import TaxonomyRetriever


PDF_PATH = str(
    REPO_ROOT
    / "data"
    / "raw"
    / "diabetes_monitoring_guidance.pdf"
)


pages = load_pdf(PDF_PATH)

chunks = create_chunks(
    pages=pages,
    document_id="diabetes",
)

retriever = TaxonomyRetriever(
    chunks=chunks,
)

results = retriever.retrieve(
    top_k=10,
)

print("=" * 80)
print("TAXONOMY RETRIEVAL")
print("=" * 80)

for index, result in enumerate(results, start=1):
    chunk = result["chunk"]

    print(
        f"{index}. "
        f"page={chunk['page_number']} | "
        f"type={chunk['section_type']}"
    )