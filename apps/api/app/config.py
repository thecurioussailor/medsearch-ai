import os
from pathlib import Path

from dotenv import load_dotenv


API_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = API_DIR.parent.parent

# Development configuration only; the file is git-ignored.
load_dotenv(API_DIR / ".env")

PDF_PATH = str(
    REPO_ROOT
    / "data"
    / "raw"
    / "diabetes_monitoring_guidance.pdf"
)

# Must match the document_id used when the Qdrant collection was indexed,
# otherwise chunk IDs from Qdrant will not match the in-memory BM25 chunks.
DOCUMENT_ID = "who-diabetes-monitoring-2024"

DEFAULT_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"


def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)

    return [
        origin.strip()
        for origin in raw.split(",")
        if origin.strip()
    ]
