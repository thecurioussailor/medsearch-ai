
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.vectorstore.qdrant_store import QdrantStore


def main():
    store = QdrantStore()
    embedder = Embedder()

    query = "Which indicators measure diabetes mortality?"
    query_vector = embedder.embed_text(query)

    results = store.search(query_vector, top_k=5)

    print(f"\nQuery: {query}")
    print(f"Results found: {len(results)}\n")

    for index, result in enumerate(results, start=1):
        chunk = result["chunk"]
        print(f"--- Result {index} ---")
        print(f"Score: {result['score']:.4f}")
        print(f"Page: {chunk['page_number']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Text: {chunk['text'][:300]}")
        print()


if __name__ == "__main__":
    main()
