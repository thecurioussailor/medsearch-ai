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

    question = "What indicator measures diabetes prevalence?"

    print("\n" + "=" * 80)
    print("DENSE RETRIEVAL DEBUG")
    print("=" * 80)

    vectors = pipeline.embedder.embed_texts(
        [
            chunk["text"]
            for chunk in pipeline.chunks
        ]
    )

    dense_results = pipeline.dense_retriever.retrieve(
        query=question,
        chunks=pipeline.chunks,
        vectors=vectors,
        top_k=15,
    )

    for index, result in enumerate(dense_results, start=1):
        chunk = result["chunk"]

        print(
            f"{index}. "
            f"page={chunk['page_number']} | "
            f"score={result['score']:.4f} | "
            f"type={chunk.get('section_type')} | "
            f"indicator={chunk.get('indicator_number')} | "
            f"{chunk.get('indicator_name', '')}"
        )


    print("\n" + "=" * 80)
    print("BM25 RETRIEVAL DEBUG")
    print("=" * 80)

    bm25_results = pipeline.bm25_retriever.retrieve(
        query=question,
        top_k=15,
    )

    for index, result in enumerate(bm25_results, start=1):
        chunk = result["chunk"]

        print(
            f"{index}. "
            f"page={chunk['page_number']} | "
            f"score={result['score']:.4f} | "
            f"type={chunk.get('section_type')} | "
            f"indicator={chunk.get('indicator_number')} | "
            f"{chunk.get('indicator_name', '')}"
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