import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app, get_pipeline


def make_result() -> dict:
    return {
        "answer": "Diabetes mortality rate.",
        "citations": [{"chunk_id": "doc-000001", "page": 80}],
        "sources": [
            {
                "score": 0.42,
                "chunk": {
                    "chunk_id": "doc-000001",
                    "page_number": 80,
                    "section_type": "indicator",
                    "indicator_number": 43,
                    "indicator_name": "Diabetes mortality rate",
                    "text": "Indicator 43 text.",
                },
            }
        ],
        "retrieval_candidates": [],
        "reranked_sources": [],
    }


class AskApiTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = MagicMock()
        self.pipeline.answer.return_value = make_result()

        app.dependency_overrides[get_pipeline] = (
            lambda: self.pipeline
        )

        # No `with` block: the real pipeline (lifespan) is not started.
        self.client = TestClient(
            app,
            raise_server_exceptions=False,
        )

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertFalse(response.json()["pipeline_ready"])

    def test_ask_returns_answer_citations_and_sources(self):
        response = self.client.post(
            "/ask",
            json={"question": "  What measures diabetes mortality?  "},
        )

        self.assertEqual(response.status_code, 200)

        body = response.json()

        self.assertEqual(body["answer"], "Diabetes mortality rate.")
        self.assertEqual(
            body["citations"],
            [{"chunk_id": "doc-000001", "page": 80}],
        )
        self.assertEqual(body["sources"][0]["page_number"], 80)
        self.assertEqual(body["sources"][0]["score"], 0.42)
        self.assertEqual(
            body["sources"][0]["indicator_name"],
            "Diabetes mortality rate",
        )

        # The question is trimmed before reaching the pipeline.
        self.pipeline.answer.assert_called_once_with(
            query="What measures diabetes mortality?"
        )

    def test_empty_question_is_rejected(self):
        response = self.client.post("/ask", json={"question": ""})

        self.assertEqual(response.status_code, 422)
        self.pipeline.answer.assert_not_called()

    def test_whitespace_question_is_rejected(self):
        response = self.client.post("/ask", json={"question": "   \n\t "})

        self.assertEqual(response.status_code, 422)
        self.pipeline.answer.assert_not_called()

    def test_missing_question_is_rejected(self):
        response = self.client.post("/ask", json={})

        self.assertEqual(response.status_code, 422)

    def test_pipeline_error_returns_500_without_internals(self):
        self.pipeline.answer.side_effect = RuntimeError(
            "secret-internal-detail sk-test"
        )

        with self.assertLogs("medsearch.api", level="ERROR"):
            response = self.client.post(
                "/ask",
                json={"question": "What measures diabetes mortality?"},
            )

        self.assertEqual(response.status_code, 500)
        self.assertNotIn("secret-internal-detail", response.text)
        self.assertNotIn("sk-test", response.text)
        self.assertIn("detail", response.json())

    def test_missing_pipeline_returns_503(self):
        app.dependency_overrides.clear()

        response = self.client.post(
            "/ask",
            json={"question": "What measures diabetes mortality?"},
        )

        self.assertEqual(response.status_code, 503)

    def test_cors_allows_local_frontend_only(self):
        allowed = self.client.options(
            "/ask",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        blocked = self.client.options(
            "/ask",
            headers={
                "Origin": "http://evil.example",
                "Access-Control-Request-Method": "POST",
            },
        )

        self.assertEqual(
            allowed.headers.get("access-control-allow-origin"),
            "http://localhost:3000",
        )
        self.assertIsNone(
            blocked.headers.get("access-control-allow-origin")
        )


if __name__ == "__main__":
    unittest.main()
