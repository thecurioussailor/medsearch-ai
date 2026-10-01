import os

from openai import OpenAI


class Generator:
    def __init__(
        self,
        model: str = "gpt-5-mini",
    ):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(
        self,
        query: str,
        context: list[dict],
    ) -> dict:

        context_text = "\n\n".join(
            [
                (
                    f"[Chunk ID: {item['chunk']['chunk_id']}]\n"
                    f"[Page: {item['chunk']['page_number']}]\n"
                    f"{item['chunk']['text']}"
                )
                for item in context
            ]
        )

        system_prompt = """
You are MedSearch AI, a medical document question-answering assistant.

Answer the user's question using ONLY the provided document context.

Rules:

1. Answer only when the provided context contains enough evidence
   to directly answer the user's question.

2. Do not use outside knowledge.

3. Do not infer missing medical facts from related information.

4. If the context only mentions a related topic but does not contain
   the specific information requested, treat the question as unanswered.

5. If the question is unanswered, say:
   "The provided document does not contain enough information
   to answer this question."

6. When the question is unanswered, return an empty citations array.

7. Do not invent facts.

8. Do not invent chunk IDs or page numbers.

9. Return valid JSON.

10. The citations array must contain ONLY chunk IDs that appear
    in the provided context.

11. Keep the answer concise and factual.

Return exactly this structure:

{
  "answer": "your answer",
  "citations": ["chunk-id-1", "chunk-id-2"]
}

For an unanswered question, return:

{
  "answer": "The provided document does not contain enough information to answer this question.",
  "citations": []
}
"""

        user_prompt = f"""
Question:
{query}

Document context:
{context_text}
"""

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_prompt,
        )

        import json

        return json.loads(response.output_text)