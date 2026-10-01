from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / "apps" / "api" / ".env")

from app.rag.pipeline import RAGPipeline


PDF_PATH = "data/raw/diabetes_monitoring_guidance.pdf"


def main():
    pipeline = RAGPipeline(
        pdf_path=PDF_PATH,
        document_id="diabetes",
    )

    question = (
        "What is the recommended dosage of metformin "
        "for adults with diabetes?"
    )

    result = pipeline.answer(
        query=question,
        top_k=5,
    )

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print("\n" + "=" * 80)
    print("CITATIONS")
    print("=" * 80)

    for citation in result["citations"]:
        print(
            f"- {citation['chunk_id']} "
            f"(Page {citation['page']})"
        )

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):
        chunk = source["chunk"]

        print(
            f"{index}. "
            f"page={chunk['page_number']} | "
            f"rrf={source['score']:.4f} | "
            f"metadata={source.get('metadata_score', 0)} | "
            f"section_bonus={source.get('section_bonus', 0):.4f} | "
            f"final={source.get('final_score', source['score']):.4f} | "
            f"type={chunk.get('section_type')} | "
            f"indicator={chunk.get('indicator_number')} | "
            f"{chunk.get('indicator_name', '')}"
        )


if __name__ == "__main__":
    main()