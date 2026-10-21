"use client";

import { useId, type SubmitEvent, type KeyboardEvent, type Ref } from "react";
import { MAX_QUESTION_LENGTH } from "@/lib/constants";
import { ArrowUpIcon, SpinnerIcon } from "./icons";

const kbdClass =
  "rounded border border-line bg-canvas px-1 py-px font-sans text-[11px] font-medium text-muted";

interface QuestionComposerProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (question: string) => void;
  /** Set while a request is in flight. Unused until the API is connected. */
  isLoading?: boolean;
  disabled?: boolean;
  error?: string | null;
  textareaRef?: Ref<HTMLTextAreaElement>;
}

export function QuestionComposer({
  value,
  onChange,
  onSubmit,
  isLoading = false,
  disabled = false,
  error = null,
  textareaRef,
}: QuestionComposerProps) {
  const id = useId();
  const inputId = `${id}-question`;
  const hintId = `${id}-hint`;
  const errorId = `${id}-error`;

  const trimmed = value.trim();
  const isLocked = disabled || isLoading;
  const canSubmit = trimmed.length > 0 && !isLocked;
  const nearLimit = value.length > MAX_QUESTION_LENGTH * 0.9;

  function submit() {
    if (isLocked) return;
    onSubmit(trimmed);
  }

  function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    submit();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    // Enter submits, Shift+Enter inserts a newline. Skip while an IME is composing.
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) {
      event.preventDefault();
      submit();
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div
        className={`rounded-2xl border bg-surface shadow-[0_1px_2px_rgba(20,24,22,0.04)] transition-[border-color,box-shadow] focus-within:ring-[3px] ${
          error
            ? "border-danger focus-within:ring-danger/10"
            : "border-line hover:border-ink/20 focus-within:border-accent/60 focus-within:ring-accent/10"
        }`}
      >
        <label htmlFor={inputId} className="sr-only">
          Your question
        </label>
        <textarea
          id={inputId}
          ref={textareaRef}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about diabetes monitoring..."
          rows={3}
          maxLength={MAX_QUESTION_LENGTH}
          readOnly={isLoading}
          disabled={disabled}
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? `${errorId} ${hintId}` : hintId}
          className="block max-h-64 min-h-22 w-full resize-none rounded-t-2xl bg-transparent px-4 pt-4 pb-2 text-base leading-relaxed text-ink caret-accent outline-none field-sizing-content placeholder:text-muted sm:px-5 disabled:cursor-not-allowed disabled:opacity-60"
        />

        <div className="flex items-center justify-between gap-3 px-3 pb-3 pl-4 sm:pl-5">
          <p id={hintId} className="min-w-0 text-xs text-muted">
            <span className="hidden sm:inline">
              <kbd className={kbdClass}>Enter</kbd> to ask ·{" "}
              <kbd className={kbdClass}>Shift</kbd> + <kbd className={kbdClass}>Enter</kbd> for a
              new line
            </span>
            <span className="sm:hidden">Answers cite their sources</span>
          </p>

          <div className="flex items-center gap-3">
            {nearLimit && (
              <span className="text-xs tabular-nums text-muted" aria-live="polite">
                {value.length}/{MAX_QUESTION_LENGTH}
              </span>
            )}
            <button
              type="submit"
              disabled={!canSubmit}
              aria-label={isLoading ? "Asking…" : "Ask question"}
              className="inline-flex h-9 shrink-0 items-center gap-1.5 rounded-lg bg-accent px-3.5 text-sm font-medium text-white shadow-[0_1px_1px_rgba(15,118,110,0.25)] transition-colors hover:bg-accent-strong focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:bg-accent/35 disabled:shadow-none"
            >
              {isLoading ? (
                <SpinnerIcon className="size-4 animate-spin" />
              ) : (
                <ArrowUpIcon className="size-4" />
              )}
              <span>Ask</span>
            </button>
          </div>
        </div>
      </div>

      {error && (
        <p id={errorId} role="alert" className="mt-2 px-1 text-sm text-danger">
          {error}
        </p>
      )}
    </form>
  );
}
