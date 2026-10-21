from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.ingestion.chunker import create_chunks
from app.ingestion.loader import load_pdf
from app.retrieval.retriever import Retriever
from app.vectorstore.qdrant_store import QdrantStore


PDF_PATH = ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"
DOCUMENT_ID = "who-diabetes-monitoring-2024"


class SpyStore(QdrantStore):
    def __init__(self):
        super().__init__()
        self.search_calls = 0

    def search(self, *args, **kwargs):
        self.search_calls += 1
        return super().search(*args, **kwargs)


def main():
    chunks = create_chunks(
        load_pdf(str(PDF_PATH)),
        document_id=DOCUMENT_ID,
    )
    local_ids = {chunk["chunk_id"] for chunk in chunks}

    store = SpyStore()
    retriever = Retriever(Embedder(), store)

    # 1. Index and local chunks must describe the same document.
    assert store.count() == len(chunks), (
        f"Qdrant has {store.count()} points, "
        f"pipeline has {len(chunks)} chunks."
    )

    # 2. Dense retrieval must go through Qdrant and return the full corpus.
    results = retriever.retrieve(
        query="Which indicators measure diabetes mortality?",
        top_k=len(chunks),
    )
    assert store.search_calls == 1, "Retriever did not call Qdrant."
    assert len(results) == len(chunks), (
        f"Expected {len(chunks)} results, got {len(results)}."
    )

    # 3. Every Qdrant hit must map to a locally built chunk (needed by RRF).
    missing = {r["chunk"]["chunk_id"] for r in results} - local_ids
    assert not missing, f"Chunk IDs missing locally: {sorted(missing)[:3]}"

    print(
        f"OK: {store.count()} points, {len(results)} results from Qdrant, "
        "all chunk IDs match."
    )


if __name__ == "__main__":
    main()
