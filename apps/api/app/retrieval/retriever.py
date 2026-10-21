
class Retriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query, chunks=None, vectors=None, top_k=5):
        query_vector = self.embedder.embed_text(query)

        return self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )
