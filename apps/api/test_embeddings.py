from app.embeddings.embedder import Embedder

embedder = Embedder()

text = "What indicators are used to monitor diabetes?"

vector = embedder.embed_text(text)

print(f"Vector dimentions: {len(vector)}")

print("\nFirst 10 values:")
print(vector[:354])