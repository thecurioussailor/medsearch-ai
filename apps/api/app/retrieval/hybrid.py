class HybridRetriever:
    def __init__(
        self,
        dense_retriever,
        bm25_retriever,
        k: int = 60,
    ):
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever
        self.k = k

    def retrieve(
        self,
        query: str,
        chunks: list[dict],
        vectors: list[list[float]],
        top_k: int = 5,
    ) -> list[dict]:

        dense_results = self.dense_retriever.retrieve(
            query=query,
            chunks=chunks,
            vectors=vectors,
            top_k=len(chunks),
        )

        bm25_results = self.bm25_retriever.retrieve(
            query=query,
            top_k=len(chunks),
        )

        fused_scores = {}

        for rank, result in enumerate(dense_results, start=1):
            chunk_id = result["chunk"]["chunk_id"]

            fused_scores[chunk_id] = fused_scores.get(
                chunk_id,
                0,
            ) + 1 / (self.k + rank)

        for rank, result in enumerate(bm25_results, start=1):
            chunk_id = result["chunk"]["chunk_id"]

            fused_scores[chunk_id] = fused_scores.get(
                chunk_id,
                0,
            ) + 1 / (self.k + rank)

        chunk_by_id = {
            chunk["chunk_id"]: chunk
            for chunk in chunks
        }

        ranked = sorted(
            fused_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        results = []

        for chunk_id, score in ranked[:top_k]:
            results.append(
                {
                    "score": score,
                    "chunk": chunk_by_id[chunk_id],
                }
            )

        return results