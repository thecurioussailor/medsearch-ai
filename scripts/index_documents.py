
from pathlib import Path
import sys

# Make the API package importable when running from the repository root.
ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "apps" / "api"
sys.path.insert(0, str(API_DIR))

from app.embeddings.embedder import Embedder
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.vectorstore.qdrant_store import QdrantStore


PDF_PATH = ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"


def main():
    print("Loading PDF...")
    pages = load_pdf(str(PDF_PATH))
    print(f"Loaded {len(pages)} pages")

    print("Creating chunks...")
    chunks = create_chunks(
        pages,
        document_id="who-diabetes-monitoring-2024",
    )
    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")
    embedder = Embedder()
    vectors = embedder.embed_texts(
        [chunk["text"] for chunk in chunks]
    )
    print(f"Generated {len(vectors)} embeddings")

    print("Indexing chunks in Qdrant...")
    store = QdrantStore()
    store.upsert_chunks(chunks, vectors)

    print(f"Qdrant now contains {store.count()} points.")


if __name__ == "__main__":
    main()
