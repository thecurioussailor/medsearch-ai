import type { AskRequest, AskResponse, Citation, Source } from "./types";

// Public base URL of the FastAPI service. Not a secret: it is inlined into the
// browser bundle at build time. The OpenAI key stays on the server.
const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"
).replace(/\/+$/, "");

// Retrieval plus an LLM call can be slow; give up after this long.
const REQUEST_TIMEOUT_MS = 90_000;

export type ApiErrorKind =
  | "network" // Backend unreachable, CORS blocked, or offline.
  | "timeout"
  | "validation" // HTTP 422
  | "unavailable" // HTTP 503: pipeline not ready
  | "server" // HTTP 5xx
  | "http" // Any other non-2xx status
  | "malformed"; // 2xx with a body that doesn't match AskResponse

export class ApiError extends Error {
  readonly kind: ApiErrorKind;
  readonly status: number | null;

  constructor(kind: ApiErrorKind, message: string, status: number | null = null) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
    this.status = status;
  }
}

function kindForStatus(status: number): ApiErrorKind {
  if (status === 422) return "validation";
  if (status === 503) return "unavailable";
  if (status >= 500) return "server";
  return "http";
}

// --- Runtime validation of the response body -------------------------------

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNullableString(value: unknown): value is string | null | undefined {
  return value == null || typeof value === "string";
}

function isCitation(value: unknown): value is Citation {
  return (
    isRecord(value) &&
    typeof value.chunk_id === "string" &&
    typeof value.page === "number"
  );
}

function isSource(value: unknown): value is Source {
  return (
    isRecord(value) &&
    typeof value.chunk_id === "string" &&
    typeof value.page_number === "number" &&
    typeof value.score === "number" &&
    typeof value.text === "string" &&
    isNullableString(value.section_type) &&
    isNullableString(value.indicator_name) &&
    (value.indicator_number == null ||
      typeof value.indicator_number === "string" ||
      typeof value.indicator_number === "number")
  );
}

function parseAskResponse(value: unknown): AskResponse | null {
  if (
    !isRecord(value) ||
    typeof value.answer !== "string" ||
    !Array.isArray(value.citations) ||
    !Array.isArray(value.sources) ||
    !value.citations.every(isCitation) ||
    !value.sources.every(isSource)
  ) {
    return null;
  }

  return {
    answer: value.answer,
    citations: value.citations,
    // Normalise optional fields that FastAPI may omit to explicit nulls.
    sources: value.sources.map((source) => ({
      ...source,
      section_type: source.section_type ?? null,
      indicator_number: source.indicator_number ?? null,
      indicator_name: source.indicator_name ?? null,
    })),
  };
}

// --- Request ----------------------------------------------------------------

export async function askQuestion(
  question: string,
  options: { signal?: AbortSignal } = {},
): Promise<AskResponse> {
  const body: AskRequest = { question };

  const timeoutSignal = AbortSignal.timeout(REQUEST_TIMEOUT_MS);
  const signal = options.signal
    ? AbortSignal.any([options.signal, timeoutSignal])
    : timeoutSignal;

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(body),
      signal,
    });
  } catch (error) {
    if (timeoutSignal.aborted) {
      throw new ApiError("timeout", "The request timed out.");
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw error; // Cancelled by the caller; not a user-facing failure.
    }
    // fetch rejects with a TypeError for network failures and CORS blocks.
    throw new ApiError("network", "Could not reach the MedSearch API.");
  }

  if (!response.ok) {
    throw new ApiError(
      kindForStatus(response.status),
      `Request failed with status ${response.status}.`,
      response.status,
    );
  }

  let json: unknown;
  try {
    json = await response.json();
  } catch {
    throw new ApiError("malformed", "The response was not valid JSON.", response.status);
  }

  const parsed = parseAskResponse(json);
  if (!parsed) {
    throw new ApiError(
      "malformed",
      "The response did not match the expected format.",
      response.status,
    );
  }

  return parsed;
}
