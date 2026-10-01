class FrameworkRetriever:
    def __init__(
        self,
        hybrid_retriever,
        taxonomy_retriever,
    ):
        self.hybrid_retriever = hybrid_retriever
        self.taxonomy_retriever = taxonomy_retriever

    def _needs_taxonomy(
        self,
        query: str,
    ) -> bool:
        query_lower = query.lower()

        taxonomy_phrases = [
            "which indicators are included",
            "what indicators are included",
            "which indicators belong",
            "what indicators belong",
            "main domains",
            "what are the domains",
            "which domains",
        ]

        return any(
            phrase in query_lower
            for phrase in taxonomy_phrases
        )

    def retrieve(
        self,
        query: str,
        chunks: list[dict],
        vectors: list[list[float]],
        top_k: int = 10,
    ) -> list[dict]:

        hybrid_results = self.hybrid_retriever.retrieve(
            query=query,
            chunks=chunks,
            vectors=vectors,
            top_k=top_k,
        )

        if not self._needs_taxonomy(query):
            return hybrid_results

        taxonomy_results = self.taxonomy_retriever.retrieve(
            top_k=4,
        )

        results_by_id = {}

        for result in hybrid_results:
            chunk_id = result["chunk"]["chunk_id"]

            results_by_id[chunk_id] = {
                **result,
                "retrieval_source": "hybrid",
            }

        for result in taxonomy_results:
            chunk_id = result["chunk"]["chunk_id"]

            if chunk_id not in results_by_id:
                results_by_id[chunk_id] = {
                    **result,
                    "retrieval_source": "taxonomy",
                }

        return list(results_by_id.values())