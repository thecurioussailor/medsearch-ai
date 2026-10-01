class TaxonomyRetriever:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks

    def retrieve(
        self,
        top_k: int = 5,
    ) -> list[dict]:

        results = []

        for chunk in self.chunks:
            if chunk.get("section_type") != "taxonomy":
                continue

            results.append(
                {
                    "score": 1.0,
                    "chunk": chunk,
                }
            )

        return results[:top_k]