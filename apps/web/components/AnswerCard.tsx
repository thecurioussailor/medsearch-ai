import type { Citation } from "@/lib/types";
import { PlusIcon } from "./icons";

export interface ResolvedCitation extends Citation {
  /** Index into the response's sources, or null if the passage wasn't returned. */
  sourceIndex: number | null;
}

interface AnswerCardProps {
  question: string;
  answer: string;
  citations: ResolvedCitation[];
  onCitationSelect: (sourceIndex: number) => void;
  onNewSearch: () => void;
}

export function AnswerCard({
  question,
  answer,
  citations,
  onCitationSelect,
  onNewSearch,
}: AnswerCardProps) {
  return (
    <article
      aria-labelledby="answer-heading"
      className="rounded-2xl border border-line bg-surface shadow-[0_1px_2px_rgba(20,24,22,0.04)]"
    >
      <header className="flex items-start justify-between gap-4 border-b border-line px-4 py-3 sm:px-5">
        <div className="min-w-0">
          <p className="text-xs font-medium text-muted">Question</p>
          <p className="mt-0.5 text-sm text-ink break-words whitespace-pre-wrap">{question}</p>
        </div>
        <button
          type="button"
          onClick={onNewSearch}
          className="inline-flex shrink-0 items-center gap-1.5 rounded-lg border border-line px-2.5 py-1.5 text-xs font-medium text-muted transition-colors hover:border-ink/20 hover:text-ink focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
        >
          <PlusIcon className="size-3.5" />
          New question
        </button>
      </header>

      <div className="px-4 py-5 sm:px-5">
        <h2 id="answer-heading" className="text-xs font-medium uppercase tracking-[0.12em] text-accent">
          Answer
        </h2>
        {/* Rendered as plain text: React escapes it, and model output is never parsed as HTML. */}
        <p className="mt-2 font-serif text-[17px] leading-relaxed text-ink break-words whitespace-pre-wrap sm:text-lg">
          {answer}
        </p>
      </div>

      <footer className="border-t border-line bg-canvas/60 px-4 py-3 sm:px-5 rounded-b-2xl">
        {citations.length > 0 ? (
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-medium text-muted">Cited passages</span>
            <ul className="flex flex-wrap gap-1.5">
              {citations.map((citation, index) => (
                <li key={citation.chunk_id}>
                  {citation.sourceIndex !== null ? (
                    <button
                      type="button"
                      onClick={() => onCitationSelect(citation.sourceIndex as number)}
                      title={`Show passage ${citation.chunk_id}`}
                      className="inline-flex items-center gap-1 rounded-md border border-accent/25 bg-accent-soft px-2 py-1 text-xs font-medium text-accent-strong transition-colors hover:border-accent/50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
                    >
                      <span aria-hidden="true">[{index + 1}]</span>
                      <span>Page {citation.page}</span>
                      <span className="sr-only">, show cited passage</span>
                    </button>
                  ) : (
                    <span
                      title={citation.chunk_id}
                      className="inline-flex items-center gap-1 rounded-md border border-line bg-surface px-2 py-1 text-xs text-muted"
                    >
                      <span aria-hidden="true">[{index + 1}]</span>
                      <span>Page {citation.page}</span>
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <p className="text-xs text-muted">No passages were cited for this answer.</p>
        )}
      </footer>
    </article>
  );
}
