class Retriever:
    def __init__(self, embedder):
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        chunks: list[dict],
        vectors: list[list[float]],
        top_k: int = 5,
    ) -> list[dict]:

        query_vector = self.embedder.embed_text(query)

        results = []

        for chunk, vector in zip(chunks, vectors):

            score = sum(
                query_value * chunk_value
                for query_value, chunk_value
                in zip(query_vector, vector)
            )

            results.append(
                {
                    "score": score,
                    "chunk": chunk,
                }
            )

        results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        return results[:top_k]