"use client";

import { useEffect, useRef, useState } from "react";
import { ApiError, askQuestion, type ApiErrorKind } from "@/lib/api";
import { SUGGESTED_QUESTIONS } from "@/lib/constants";
import type { AskResponse } from "@/lib/types";
import { SpinnerIcon } from "./icons";
import { QuestionComposer } from "./QuestionComposer";
import { SearchError } from "./SearchError";
import { SearchResult } from "./SearchResult";
import { SuggestedQuestions } from "./SuggestedQuestions";

type SearchState =
  | { status: "idle" }
  | { status: "loading"; id: number; question: string }
  | { status: "success"; id: number; question: string; response: AskResponse }
  | {
      status: "error";
      id: number;
      question: string;
      kind: ApiErrorKind;
      httpStatus: number | null;
    };

export function SearchWorkspace() {
  const [question, setQuestion] = useState("");
  const [inputError, setInputError] = useState<string | null>(null);
  const [search, setSearch] = useState<SearchState>({ status: "idle" });
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Guards against double submits that land before React re-renders.
  const inFlightRef = useRef(false);
  const requestIdRef = useRef(0);
  const abortRef = useRef<AbortController | null>(null);

  // Cancel any in-flight request if the component unmounts.
  useEffect(() => () => abortRef.current?.abort(), []);

  const isLoading = search.status === "loading";

  function focusComposer(caretAtEnd?: number) {
    requestAnimationFrame(() => {
      const textarea = textareaRef.current;
      if (!textarea) return;
      textarea.focus();
      if (caretAtEnd !== undefined) textarea.setSelectionRange(caretAtEnd, caretAtEnd);
    });
  }

  async function runSearch(value: string) {
    if (inFlightRef.current) return;
    inFlightRef.current = true;

    const id = ++requestIdRef.current;
    const controller = new AbortController();
    abortRef.current = controller;
    setSearch({ status: "loading", id, question: value });

    try {
      const response = await askQuestion(value, { signal: controller.signal });
      if (requestIdRef.current !== id) return;
      setSearch({ status: "success", id, question: value, response });
    } catch (error) {
      if (controller.signal.aborted || requestIdRef.current !== id) return;
      const apiError =
        error instanceof ApiError ? error : new ApiError("network", "Request failed.");
      setSearch({
        status: "error",
        id,
        question: value,
        kind: apiError.kind,
        httpStatus: apiError.status,
      });
    } finally {
      if (requestIdRef.current === id) {
        inFlightRef.current = false;
        abortRef.current = null;
      }
    }
  }

  function handleChange(value: string) {
    setQuestion(value);
    if (inputError && value.trim()) setInputError(null);
  }

  function handleSubmit(value: string) {
    if (!value) {
      setInputError("Enter a question to search the guidance.");
      return;
    }
    setInputError(null);
    void runSearch(value);
  }

  function handleRetry() {
    if (search.status === "error") void runSearch(search.question);
  }

  function handleNewSearch() {
    setSearch({ status: "idle" });
    setQuestion("");
    focusComposer();
  }

  function handleSelectSuggestion(value: string) {
    setQuestion(value);
    setInputError(null);
    focusComposer(value.length);
  }

  return (
    <div>
      <QuestionComposer
        value={question}
        onChange={handleChange}
        onSubmit={handleSubmit}
        isLoading={isLoading}
        error={inputError}
        textareaRef={textareaRef}
      />

      {/* Stays mounted so screen readers announce loading and completion. */}
      <div role="status" aria-live="polite" className="sr-only">
        {search.status === "loading" && "Searching the source document…"}
        {search.status === "success" && "Answer ready."}
      </div>

      <div aria-busy={isLoading}>
        {search.status === "loading" && (
          <div className="mt-4 flex items-center gap-3 rounded-xl border border-line bg-surface px-4 py-3.5 text-sm text-muted sm:px-5">
            <SpinnerIcon className="size-4 shrink-0 animate-spin text-accent motion-reduce:animate-none" />
            <span>Searching the source document…</span>
          </div>
        )}

        {search.status === "error" && (
          <div className="mt-4">
            <SearchError kind={search.kind} status={search.httpStatus} onRetry={handleRetry} />
          </div>
        )}

        {search.status === "success" && (
          <div className="mt-6">
            <SearchResult
              key={search.id}
              question={search.question}
              response={search.response}
              onNewSearch={handleNewSearch}
            />
          </div>
        )}
      </div>

      {search.status !== "success" && (
        <div className="mt-6">
          <SuggestedQuestions
            questions={SUGGESTED_QUESTIONS}
            onSelect={handleSelectSuggestion}
            disabled={isLoading}
          />
        </div>
      )}
    </div>
  );
}
