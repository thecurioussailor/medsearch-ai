import sys
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

load_dotenv(REPO_ROOT / "apps" / "api" / ".env")


from app.rag.pipeline import RAGPipeline
from evaluation.rag_questions import EVALUATION_QUESTIONS


PDF_PATH = str(
    REPO_ROOT
    / "data"
    / "raw"
    / "diabetes_monitoring_guidance.pdf"
)

DOCUMENT_ID = "who-diabetes-monitoring-2024"


def recall_at_k(
    candidate_pages,
    expected_pages,
    k,
):
    top_pages = candidate_pages[:k]

    expected = set(expected_pages)
    retrieved = set(top_pages)

    if not expected:
        return 0.0

    return len(expected & retrieved) / len(expected)


def reciprocal_rank(
    candidate_pages,
    expected_pages,
):
    expected = set(expected_pages)

    for rank, page in enumerate(
        candidate_pages,
        start=1,
    ):
        if page in expected:
            return 1 / rank

    return 0.0


def evaluate_question(
    pipeline,
    test_case,
):
    result = pipeline.answer(
        query=test_case["question"],
        top_k=5,
    )

    retrieval_candidates = result.get(
        "retrieval_candidates",
        []
    )

    reranked_sources = result.get(
        "reranked_sources",
        []
    )

    candidate_pages = [
        item["chunk"]["page_number"]
        for item in retrieval_candidates
    ]

    reranked_pages = [
        item["chunk"]["page_number"]
        for item in reranked_sources
    ]

    returned_pages = [
        citation["page"]
        for citation in result["citations"]
    ]

    expected_pages = test_case["expected_pages"]

    expected_citation_pages = test_case[
        "expected_citation_pages"
    ]

    if test_case["type"] == "answerable":
        retrieval_passed = any(
            page in returned_pages
            for page in expected_pages
        )

        citation_mode = test_case.get(
            "citation_mode",
            "exact",
        )

        if citation_mode == "exact":
            citation_passed = (
                set(returned_pages)
                == set(expected_citation_pages)
            )

        elif citation_mode == "subset":
            citation_passed = (
                len(returned_pages) > 0
                and set(returned_pages).issubset(
                    set(expected_citation_pages)
                )
            )

        else:
            raise ValueError(
                f"Unknown citation mode: {citation_mode}"
            )

        passed = (
            retrieval_passed
            and citation_passed
        )

    else:
        retrieval_passed = (
            len(returned_pages) == 0
        )

        citation_passed = (
            len(returned_pages) == 0
        )

        passed = (
            retrieval_passed
            and citation_passed
        )

    recall_5 = None
    recall_10 = None
    recall_20 = None
    mrr = None

    if test_case["type"] == "answerable":
        recall_5 = recall_at_k(
            candidate_pages,
            expected_pages,
            5,
        )

        recall_10 = recall_at_k(
            candidate_pages,
            expected_pages,
            10,
        )

        recall_20 = recall_at_k(
            candidate_pages,
            expected_pages,
            20,
        )

        mrr = reciprocal_rank(
            candidate_pages,
            expected_pages,
        )

    return {
        "id": test_case["id"],
        "question": test_case["question"],
        "type": test_case["type"],
        "expected_pages": expected_pages,
        "expected_citation_pages": (
            expected_citation_pages
        ),
        "candidate_pages": candidate_pages,
        "reranked_pages": reranked_pages,
        "returned_pages": returned_pages,
        "recall_at_5": recall_5,
        "recall_at_10": recall_10,
        "recall_at_20": recall_20,
        "mrr": mrr,
        "retrieval_passed": retrieval_passed,
        "citation_passed": citation_passed,
        "passed": passed,
        "answer": result["answer"],
    }


def main():
    print("=" * 80)
    print("MEDSEARCH AI — RAG EVALUATION")
    print("=" * 80)

    pipeline = RAGPipeline(
        pdf_path=PDF_PATH,
        document_id=DOCUMENT_ID,
    )

    results = []

    for test_case in EVALUATION_QUESTIONS:
        print(
            f"\nRunning {test_case['id']}..."
        )

        result = evaluate_question(
            pipeline,
            test_case,
        )

        results.append(result)

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(f"{status}")

        print(
            f"Question: "
            f"{result['question']}"
        )

        print(
            f"Expected pages: "
            f"{result['expected_pages']}"
        )

        print(
            f"Expected citation pages: "
            f"{result['expected_citation_pages']}"
        )

        print(
            f"Candidate pages: "
            f"{result['candidate_pages']}"
        )

        print(
            f"Reranked pages: "
            f"{result['reranked_pages']}"
        )

        print(
            f"Returned pages: "
            f"{result['returned_pages']}"
        )

        print(
            f"Retrieval: "
            f"{'PASS' if result['retrieval_passed'] else 'FAIL'}"
        )

        print(
            f"Citations: "
            f"{'PASS' if result['citation_passed'] else 'FAIL'}"
        )

        if result["type"] == "answerable":
            print(
                f"Recall@5: "
                f"{result['recall_at_5']:.2%}"
            )

            print(
                f"Recall@10: "
                f"{result['recall_at_10']:.2%}"
            )

            print(
                f"Recall@20: "
                f"{result['recall_at_20']:.2%}"
            )

            print(
                f"MRR: "
                f"{result['mrr']:.4f}"
            )

        print(
            f"Answer: "
            f"{result['answer']}"
        )

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    total = len(results)

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)

    print(
        f"Passed: {passed}/{total}"
    )

    accuracy = (
        (passed / total) * 100
        if total
        else 0
    )

    print(
        f"Accuracy: {accuracy:.2f}%"
    )

    answerable_results = [
        result
        for result in results
        if result["type"] == "answerable"
    ]

    if answerable_results:
        avg_recall_5 = sum(
            result["recall_at_5"]
            for result in answerable_results
        ) / len(answerable_results)

        avg_recall_10 = sum(
            result["recall_at_10"]
            for result in answerable_results
        ) / len(answerable_results)

        avg_recall_20 = sum(
            result["recall_at_20"]
            for result in answerable_results
        ) / len(answerable_results)

        avg_mrr = sum(
            result["mrr"]
            for result in answerable_results
        ) / len(answerable_results)

        print()

        print(
            f"Recall@5:  "
            f"{avg_recall_5:.2%}"
        )

        print(
            f"Recall@10: "
            f"{avg_recall_10:.2%}"
        )

        print(
            f"Recall@20: "
            f"{avg_recall_20:.2%}"
        )

        print(
            f"MRR:       "
            f"{avg_mrr:.4f}"
        )

    print("=" * 80)


if __name__ == "__main__":
    main()