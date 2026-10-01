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

DOCUMENT_ID = "diabetes"


def evaluate_question(pipeline, test_case):
    result = pipeline.answer(
        query=test_case["question"],
        top_k=5,
    )

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

    return {
        "id": test_case["id"],
        "question": test_case["question"],
        "type": test_case["type"],
        "expected_pages": expected_pages,
        "expected_citation_pages": (
            expected_citation_pages
        ),
        "returned_pages": returned_pages,
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

    print("=" * 80)


if __name__ == "__main__":
    main()