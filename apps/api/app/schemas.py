from typing import Annotated

from pydantic import BaseModel, StringConstraints


class AskRequest(BaseModel):
    question: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=1000,
        ),
    ]


class Citation(BaseModel):
    chunk_id: str
    page: int


class Source(BaseModel):
    chunk_id: str
    page_number: int
    score: float
    section_type: str | None = None
    indicator_number: int | str | None = None
    indicator_name: str | None = None
    text: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    sources: list[Source]


class HealthResponse(BaseModel):
    status: str
    pipeline_ready: bool
    openai_key_configured: bool
