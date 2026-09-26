from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.embeddings.embedder import Embedder
from app.retrieval.retriever import Retriever


PDF_PATH = "../../data/raw/diabetes_monitoring_guidance.pdf"

DOCUMENT_ID = "who-diabetes-monitoring-2024"


pages = load_pdf(PDF_PATH)

chunks = create_chunks(
    pages,
    document_id=DOCUMENT_ID,
)

embedder = Embedder()

texts = [chunk["text"] for chunk in chunks]

vectors = embedder.embed_texts(texts)

retriever = Retriever(embedder)


queries = [
    "What indicators are used to monitor diabetes?",
    "What are the risk factors for diabetes?",
    "How is diabetes prevalence monitored?",
    "What indicators measure diabetes service delivery?",
    "What are the global diabetes coverage targets?",
]


for query in queries:

    print("\n")
    print("=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    results = retriever.retrieve(
        query=query,
        chunks=chunks,
        vectors=vectors,
        top_k=3,
    )

    for rank, result in enumerate(results, start=1):

        chunk = result["chunk"]

        print("\n" + "-" * 100)
        print(f"RANK: {rank}")
        print(f"SCORE: {result['score']:.4f}")
        print(f"PAGE: {chunk['page_number']}")
        print(f"CHUNK: {chunk['chunk_id']}")
        print("-" * 100)

        print(chunk["text"][:400])