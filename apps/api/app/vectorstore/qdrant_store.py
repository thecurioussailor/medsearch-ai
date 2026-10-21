
from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient, models


class QdrantStore:
    def __init__(
        self,
        collection_name: str = "medsearch_chunks",
        url: str = "http://localhost:6333",
        vector_size: int = 384,
    ):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def ensure_collection(self) -> None:
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert_chunks(
        self,
        chunks: list[dict],
        vectors: list[list[float]],
    ) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("Each chunk must have exactly one vector.")

        self.ensure_collection()
        points = []

        for chunk, vector in zip(chunks, vectors):
            if len(vector) != self.vector_size:
                raise ValueError(
                    f"Expected {self.vector_size} dimensions, "
                    f"received {len(vector)}."
                )

            # Qdrant point IDs must be integers or UUIDs.
            point_id = str(
                uuid5(NAMESPACE_URL, chunk["chunk_id"])
            )

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=chunk,
                )
            )

        # Upsert in batches to avoid sending an unnecessarily
        # large request if the corpus grows.
        batch_size = 64
        for start in range(0, len(points), batch_size):
            self.client.upsert(
                collection_name=self.collection_name,
                points=points[start : start + batch_size],
                wait=True,
            )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        self.ensure_collection()

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        )

        results = []
        for point in response.points:
            if point.payload is None:
                continue

            results.append(
                {
                    "score": float(point.score),
                    "chunk": point.payload,
                }
            )

        return results

    def count(self) -> int:
        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )
        return result.count
