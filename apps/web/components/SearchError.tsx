import type { ApiErrorKind } from "@/lib/api";
import { AlertIcon, RefreshIcon } from "./icons";

const MESSAGES: Record<ApiErrorKind, { title: string; body: string }> = {
  network: {
    title: "Can’t reach the search service",
    body: "The MedSearch API didn’t respond. Check that the backend is running and that this site is allowed to connect to it, then try again.",
  },
  timeout: {
    title: "The search took too long",
    body: "No response arrived in time. The service may be busy. Please try again.",
  },
  validation: {
    title: "The question couldn’t be processed",
    body: "Questions must be between 1 and 1,000 characters. Edit your question and try again.",
  },
  unavailable: {
    title: "Search is still starting up",
    body: "The search service is running but not ready to answer yet. Wait a moment, then try again.",
  },
  server: {
    title: "Something went wrong generating an answer",
    body: "The search service ran into a problem. Please try again.",
  },
  http: {
    title: "The request was rejected",
    body: "The search service couldn’t handle this request. Please try again.",
  },
  malformed: {
    title: "Received an unexpected response",
    body: "The search service replied in a format this page doesn’t recognise, so no answer is shown.",
  },
};

interface SearchErrorProps {
  kind: ApiErrorKind;
  status: number | null;
  onRetry: () => void;
}

export function SearchError({ kind, status, onRetry }: SearchErrorProps) {
  const { title, body } = MESSAGES[kind];

  return (
    <div
      role="alert"
      className="flex flex-col gap-3 rounded-xl border border-danger/25 bg-surface px-4 py-4 sm:flex-row sm:items-start sm:px-5"
    >
      <AlertIcon className="mt-0.5 size-4 shrink-0 text-danger" />
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-ink">{title}</p>
        <p className="mt-1 text-sm leading-relaxed text-muted">{body}</p>
        {status !== null && (
          <p className="mt-1.5 text-xs text-muted">Status code {status}</p>
        )}
      </div>
      <button
        type="button"
        onClick={onRetry}
        className="inline-flex shrink-0 items-center gap-1.5 self-start rounded-lg border border-line bg-surface px-3 py-1.5 text-sm font-medium text-ink transition-colors hover:border-ink/20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
      >
        <RefreshIcon className="size-3.5" />
        Try again
      </button>
    </div>
  );
}
