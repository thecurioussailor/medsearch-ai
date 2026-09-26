import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.embeddings.embedder import Embedder
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.retrieval.retriever import Retriever


PDF_PATH = REPO_ROOT / "data" / "raw" / "diabetes_monitoring_guidance.pdf"
QUESTIONS_PATH = REPO_ROOT / "evaluation" / "questions.json"


def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
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
    retriever = Retriever(embedder)

    print("Generating embeddings...")

    texts = [chunk["text"] for chunk in chunks]
    vectors = embedder.embed_texts(texts)

    recall_at_3 = 0
    recall_at_5 = 0

    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION")
    print("=" * 60)

    for question in questions:
        results = retriever.retrieve(
            query=question["question"],
            chunks=chunks,
            vectors=vectors,
            top_k=5,
        )

        expected_pages = set(question["expected_pages"])

        top_3_pages = {
            result["chunk"]["page_number"]
            for result in results[:3]
        }

        top_5_pages = {
            result["chunk"]["page_number"]
            for result in results[:5]
        }

        hit_at_3 = bool(expected_pages & top_3_pages)
        hit_at_5 = bool(expected_pages & top_5_pages)

        if hit_at_3:
            recall_at_3 += 1

        if hit_at_5:
            recall_at_5 += 1

        print(f"\n{question['id']}: {question['question']}")
        print(f"Expected pages: {sorted(expected_pages)}")
        print(f"Top 3 pages:   {sorted(top_3_pages)}")
        print(f"Top 5 pages:   {sorted(top_5_pages)}")
        print(f"Recall@3:      {'PASS' if hit_at_3 else 'FAIL'}")
        print(f"Recall@5:      {'PASS' if hit_at_5 else 'FAIL'}")

    total = len(questions)

    recall_at_3_score = recall_at_3 / total
    recall_at_5_score = recall_at_5 / total

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(
        f"Recall@3: {recall_at_3}/{total} "
        f"({recall_at_3_score:.2%})"
    )

    print(
        f"Recall@5: {recall_at_5}/{total} "
        f"({recall_at_5_score:.2%})"
    )


if __name__ == "__main__":
    main()