class MultiQueryRetriever:
    def __init__(
        self,
        retriever,
        query_expander,
    ):
        self.retriever = retriever
        self.query_expander = query_expander

    def retrieve(
        self,
        query: str,
        chunks: list[dict],
        vectors: list[list[float]],
        top_k: int = 5,
    ) -> list[dict]:

        queries = self.query_expander.expand(query)

        scores = {}

        for expanded_query in queries:
            results = self.retriever.retrieve(
                query=expanded_query,
                chunks=chunks,
                vectors=vectors,
                top_k=10,
            )

            for rank, result in enumerate(results, start=1):
                chunk_id = result["chunk"]["chunk_id"]

                # Give higher weight to higher-ranked results.
                score = 1 / rank

                scores[chunk_id] = (
                    scores.get(chunk_id, 0) + score
                )

        chunk_by_id = {
            chunk["chunk_id"]: chunk
            for chunk in chunks
        }

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            {
                "score": score,
                "chunk": chunk_by_id[chunk_id],
            }
            for chunk_id, score in ranked[:top_k]
        ]