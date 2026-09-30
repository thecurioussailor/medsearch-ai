class MetadataReranker:
    def __init__(self):
        pass

    def _detect_intent(self, query: str) -> str:
        query_lower = query.lower()

        category_phrases = [
            "which indicators are included",
            "which indicators belong",
            "what indicators are included",
            "what indicators belong",
        ]

        overview_phrases = [
            "what indicators are used",
            "which indicators are used",
            "what indicators monitor",
            "which indicators monitor",
            "what does the indicator framework",
            "what is the indicator framework",
        ]

        for phrase in category_phrases:
            if phrase in query_lower:
                return "category"

        for phrase in overview_phrases:
            if phrase in query_lower:
                return "overview"

        return "lookup"

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        intent = self._detect_intent(query)

        query_terms = set(
            query.lower().split()
        )

        reranked = []

        for result in results:
            chunk = result["chunk"]

            metadata_text = " ".join(
                [
                    chunk.get("domain", ""),
                    chunk.get("subdomain", ""),
                    chunk.get("indicator_name", ""),
                ]
            ).lower()

            metadata_terms = set(
                metadata_text.split()
            )

            overlap = query_terms & metadata_terms

            metadata_score = len(overlap)

            section_bonus = 0.0

            if intent == "category":
                if chunk.get("section_type") == "taxonomy":
                    section_bonus = 0.05
            
            elif intent == "overview":
                if chunk.get("section_type") == "taxonomy":
                    section_bonus = 0.03

            elif intent == "lookup":
                if chunk.get("section_type") == "indicator":
                    section_bonus = 0.01

            final_score = (
                result["score"]
                + (0.01 * metadata_score)
                + section_bonus
            )

            reranked.append(
                {
                    **result,
                    "metadata_score": metadata_score,
                    "section_bonus": section_bonus,
                    "intent": intent,
                    "final_score": final_score,
                }
            )

        reranked.sort(
            key=lambda result: result["final_score"],
            reverse=True,
        )

        return reranked[:top_k]