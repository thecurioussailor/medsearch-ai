import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.retriever import Retriever
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever


PDF_PATH = REPO_ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"
QUESTIONS_PATH = REPO_ROOT / "evaluation" / "questions.json"


def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate():
    questions = load_questions()

    print("Loading document...")

    pages = load_pdf(PDF_PATH)

    chunks = create_chunks(
        pages,
        document_id="who-diabetes-monitoring-2024",
    )

    print(f"Total chunks: {len(chunks)}")

    print("Loading embedding model...")

    embedder = Embedder()

    print("Generating embeddings...")

    texts = [chunk["text"] for chunk in chunks]
    vectors = embedder.embed_texts(texts)

    dense_retriever = Retriever(embedder)
    bm25_retriever = BM25Retriever(chunks)

    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        bm25_retriever=bm25_retriever,
    )

    dense_at_3 = 0
    dense_at_5 = 0

    bm25_at_3 = 0
    bm25_at_5 = 0

    hybrid_at_3 = 0
    hybrid_at_5 = 0

    print("\n" + "=" * 80)
    print("RETRIEVAL COMPARISON")
    print("=" * 80)

    for question in questions:
        expected_pages = set(question["expected_pages"])

        dense_results = dense_retriever.retrieve(
            query=question["question"],
            chunks=chunks,
            vectors=vectors,
            top_k=5,
        )

        bm25_results = bm25_retriever.retrieve(
            query=question["question"],
            top_k=5,
        )

        hybrid_results = hybrid_retriever.retrieve(
            query=question["question"],
            chunks=chunks,
            vectors=vectors,
            top_k=5,
        )

        dense_pages_3 = {
            result["chunk"]["page_number"]
            for result in dense_results[:3]
        }

        dense_pages_5 = {
            result["chunk"]["page_number"]
            for result in dense_results[:5]
        }

        bm25_pages_3 = {
            result["chunk"]["page_number"]
            for result in bm25_results[:3]
        }

        bm25_pages_5 = {
            result["chunk"]["page_number"]
            for result in bm25_results[:5]
        }

        hybrid_pages_3 = {
            result["chunk"]["page_number"]
            for result in hybrid_results[:3]
        }

        hybrid_pages_5 = {
            result["chunk"]["page_number"]
            for result in hybrid_results[:5]
        }

        dense_hit_3 = bool(expected_pages & dense_pages_3)
        dense_hit_5 = bool(expected_pages & dense_pages_5)

        bm25_hit_3 = bool(expected_pages & bm25_pages_3)
        bm25_hit_5 = bool(expected_pages & bm25_pages_5)

        hybrid_hit_3 = bool(expected_pages & hybrid_pages_3)
        hybrid_hit_5 = bool(expected_pages & hybrid_pages_5)

        dense_at_3 += dense_hit_3
        dense_at_5 += dense_hit_5

        bm25_at_3 += bm25_hit_3
        bm25_at_5 += bm25_hit_5

        hybrid_at_3 += hybrid_hit_3
        hybrid_at_5 += hybrid_hit_5

        print(f"\n{question['id']}: {question['question']}")
        print(f"Expected: {sorted(expected_pages)}")

        print(
            f"Dense  @3: {sorted(dense_pages_3)} "
            f"{'PASS' if dense_hit_3 else 'FAIL'}"
        )

        print(
            f"BM25   @3: {sorted(bm25_pages_3)} "
            f"{'PASS' if bm25_hit_3 else 'FAIL'}"
        )

        print(
            f"Hybrid @3: {sorted(hybrid_pages_3)} "
            f"{'PASS' if hybrid_hit_3 else 'FAIL'}"
        )

        print(
            f"Dense  @5: {sorted(dense_pages_5)} "
            f"{'PASS' if dense_hit_5 else 'FAIL'}"
        )

        print(
            f"BM25   @5: {sorted(bm25_pages_5)} "
            f"{'PASS' if bm25_hit_5 else 'FAIL'}"
        )

        print(
            f"Hybrid @5: {sorted(hybrid_pages_5)} "
            f"{'PASS' if hybrid_hit_5 else 'FAIL'}"
        )

    total = len(questions)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(
        f"Dense  Recall@3: "
        f"{dense_at_3}/{total} ({dense_at_3 / total:.2%})"
    )

    print(
        f"Dense  Recall@5: "
        f"{dense_at_5}/{total} ({dense_at_5 / total:.2%})"
    )

    print(
        f"BM25   Recall@3: "
        f"{bm25_at_3}/{total} ({bm25_at_3 / total:.2%})"
    )

    print(
        f"BM25   Recall@5: "
        f"{bm25_at_5}/{total} ({bm25_at_5 / total:.2%})"
    )

    print(
        f"Hybrid Recall@3: "
        f"{hybrid_at_3}/{total} ({hybrid_at_3 / total:.2%})"
    )

    print(
        f"Hybrid Recall@5: "
        f"{hybrid_at_5}/{total} ({hybrid_at_5 / total:.2%})"
    )


if __name__ == "__main__":
    evaluate()