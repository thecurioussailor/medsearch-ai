// Mirrors the request/response schemas in apps/api/app/schemas.py.
// Kept here so the UI is typed against the real contract once /ask is wired up.

export interface AskRequest {
  question: string;
}

export interface Citation {
  chunk_id: string;
  page: number;
}

export interface Source {
  chunk_id: string;
  page_number: number;
  score: number;
  section_type: string | null;
  indicator_number: number | string | null;
  indicator_name: string | null;
  text: string;
}

export interface AskResponse {
  answer: string;
  citations: Citation[];
  sources: Source[];
}

export interface HealthResponse {
  status: string;
  pipeline_ready: boolean;
  openai_key_configured: boolean;
}
