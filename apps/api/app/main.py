import logging
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import DOCUMENT_ID, PDF_PATH, get_cors_origins
from app.schemas import AskRequest, AskResponse, HealthResponse, Source


logger = logging.getLogger("medsearch.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Imported here so importing app.main stays cheap (no model loading).
    from app.rag.pipeline import RAGPipeline

    # Built once at startup: loads the PDF, the embedding model and BM25.
    app.state.pipeline = RAGPipeline(
        pdf_path=PDF_PATH,
        document_id=DOCUMENT_ID,
    )

    yield


app = FastAPI(
    title="MedSearch AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def get_pipeline(request: Request):
    pipeline = getattr(request.app.state, "pipeline", None)

    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="The RAG pipeline is not ready.",
        )

    return pipeline


def _to_source(result: dict) -> Source:
    chunk = result["chunk"]

    return Source(
        chunk_id=chunk["chunk_id"],
        page_number=chunk["page_number"],
        score=float(result["score"]),
        section_type=chunk.get("section_type"),
        indicator_number=chunk.get("indicator_number"),
        indicator_name=chunk.get("indicator_name"),
        text=chunk["text"],
    )


@app.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    return HealthResponse(
        status="ok",
        pipeline_ready=(
            getattr(request.app.state, "pipeline", None)
            is not None
        ),
        openai_key_configured=bool(os.getenv("OPENAI_API_KEY")),
    )


# Plain `def` on purpose: answer() blocks on retrieval and the OpenAI call,
# so FastAPI runs it in a worker thread instead of the event loop.
@app.post("/ask", response_model=AskResponse)
def ask(
    body: AskRequest,
    pipeline=Depends(get_pipeline),
) -> AskResponse:
    try:
        result = pipeline.answer(query=body.question)
    except Exception:
        # Log the traceback server-side only; never echo the question,
        # document text or internals back to the client.
        logger.exception("Failed to answer a question.")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Please try again.",
        )

    return AskResponse(
        answer=result["answer"],
        citations=result["citations"],
        sources=[_to_source(item) for item in result["sources"]],
    )
