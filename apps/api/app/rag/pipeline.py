from app.generation.generator import Generator
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.embeddings.embedder import Embedder
from app.retrieval.retriever import Retriever
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.metadata_reranker import MetadataReranker
from app.retrieval.taxonomy import TaxonomyRetriever
from app.retrieval.framework import FrameworkRetriever


class RAGPipeline:
    def __init__(
        self,
        pdf_path: str,
        document_id: str,
    ):
        self.pdf_path = pdf_path
        self.document_id = document_id

        print("Loading document...")

        pages = load_pdf(pdf_path)

        self.chunks = create_chunks(
            pages=pages,
            document_id=document_id,
        )

        print(f"Loaded {len(self.chunks)} chunks.")

        print("Loading embedding model...")

        self.embedder = Embedder()

        self.dense_retriever = Retriever(
            embedder=self.embedder,
        )

        self.bm25_retriever = BM25Retriever(
            chunks=self.chunks,
        )

        self.hybrid_retriever = HybridRetriever(
            dense_retriever=self.dense_retriever,
            bm25_retriever=self.bm25_retriever,
        )

        self.taxonomy_retriever = TaxonomyRetriever(
            chunks=self.chunks,
        )

        self.framework_retriever = FrameworkRetriever(
            hybrid_retriever=self.hybrid_retriever,
            taxonomy_retriever=self.taxonomy_retriever,
        )

        self.metadata_reranker = MetadataReranker()

        self.generator = Generator()

    def answer(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:

        vectors = self.embedder.embed_texts(
            [
                chunk["text"]
                for chunk in self.chunks
            ]
        )

        retrieved = self.framework_retriever.retrieve(
            query=query,
            chunks=self.chunks,
            vectors=vectors,
            top_k=10,
        )


        print("\n" + "=" * 80)
        print("HYBRID RETRIEVAL DEBUG")
        print("=" * 80)

        for index, result in enumerate(retrieved, start=1):
            chunk = result["chunk"]

            print(
                f"{index}. "
                f"page={chunk['page_number']} | "
                f"rrf={result['score']:.4f} | "
                f"type={chunk.get('section_type')} | "
                f"indicator={chunk.get('indicator_number')} | "
                f"{chunk.get('indicator_name', '')}"
            )


        reranked = self.metadata_reranker.rerank(
            query=query,
            results=retrieved,
            top_k=top_k,
        )

        generation = self.generator.generate(
            query=query,
            context=reranked,
        )

        chunk_by_id = {
            result["chunk"]["chunk_id"]: result["chunk"]
            for result in reranked
        }

        verified_citations = []

        for chunk_id in generation.get("citations", []):
            chunk = chunk_by_id.get(chunk_id)

            if chunk is None:
                continue

            verified_citations.append(
                {
                    "chunk_id": chunk_id,
                    "page": chunk["page_number"],
                }
            )

        return {
            "answer": generation["answer"],
            "citations": verified_citations,
            "sources": reranked,
        }