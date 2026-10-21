
from app.vectorstore.qdrant_store import QdrantStore


def main():
    store = QdrantStore()
    store.ensure_collection()

    print("Qdrant connected successfully!")
    print("Collection:", store.collection_name)
    print("Existing points:", store.count())


if __name__ == "__main__":
    main()
