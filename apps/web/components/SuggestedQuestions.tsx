import { SearchIcon } from "./icons";

interface SuggestedQuestionsProps {
  questions: readonly string[];
  onSelect: (question: string) => void;
  disabled?: boolean;
}

export function SuggestedQuestions({
  questions,
  onSelect,
  disabled = false,
}: SuggestedQuestionsProps) {
  return (
    <section aria-labelledby="suggestions-heading">
      <h2 id="suggestions-heading" className="px-1 text-xs font-medium text-muted">
        Try a question
      </h2>
      <ul className="mt-2.5 grid grid-cols-1 gap-2.5 sm:grid-cols-2">
        {questions.map((question) => (
          <li key={question} className="flex">
            <button
              type="button"
              onClick={() => onSelect(question)}
              disabled={disabled}
              className="group flex min-h-16 w-full items-center gap-3 rounded-xl border border-line bg-surface px-4 py-3 text-left text-sm leading-snug text-ink transition-colors hover:border-accent/35 hover:bg-accent-soft focus-visible:border-accent/60 focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-accent/15 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <span className="flex size-7 shrink-0 items-center justify-center rounded-md bg-canvas text-muted ring-1 ring-line transition-colors group-hover:bg-surface group-hover:text-accent">
                <SearchIcon className="size-3.5" />
              </span>
              <span>{question}</span>
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
