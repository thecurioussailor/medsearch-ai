from fastapi import FastAPI

app = FastAPI(
    title="MedSearch AI",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }