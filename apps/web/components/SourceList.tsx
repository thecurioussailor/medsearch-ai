import type { Source } from "@/lib/types";
import { describeSource, formatSectionType } from "@/lib/format";
import { ChevronDownIcon } from "./icons";

interface SourceListProps {
  sources: Source[];
  /** chunk_id -> citation number shown in the answer ([1], [2], ...). */
  citationNumbers: ReadonlyMap<string, number>;
  openIndexes: ReadonlySet<number>;
  activeIndex: number | null;
  onToggle: (index: number, open: boolean) => void;
  getItemId: (index: number) => string;
}

export function SourceList({
  sources,
  citationNumbers,
  openIndexes,
  activeIndex,
  onToggle,
  getItemId,
}: SourceListProps) {
  return (
    <section aria-labelledby="sources-heading">
      <div className="flex items-baseline justify-between gap-3 px-1">
        <h2 id="sources-heading" className="text-sm font-medium text-ink">
          Retrieved passages
          <span className="ml-1.5 font-normal text-muted">({sources.length})</span>
        </h2>
        <p className="text-xs text-muted">In the order the search service returned them</p>
      </div>

      {sources.length === 0 ? (
        <p className="mt-3 rounded-xl border border-line bg-surface px-4 py-3 text-sm text-muted">
          No passages were returned for this question.
        </p>
      ) : (
        <ol className="mt-3 flex flex-col gap-2">
          {sources.map((source, index) => {
            const citationNumber = citationNumbers.get(source.chunk_id);
            const heading = describeSource(source);
            const sectionLabel = formatSectionType(source.section_type);
            const isActive = activeIndex === index;

            return (
              <li key={`${source.chunk_id}-${index}`} id={getItemId(index)} className="scroll-mt-6">
                <details
                  open={openIndexes.has(index)}
                  onToggle={(event) => onToggle(index, event.currentTarget.open)}
                  className={`group rounded-xl border bg-surface transition-colors ${
                    isActive ? "border-accent/50 ring-[3px] ring-accent/10" : "border-line"
                  }`}
                >
                  <summary className="flex cursor-pointer list-none items-start gap-3 rounded-xl px-4 py-3 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent [&::-webkit-details-marker]:hidden">
                    <span className="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-md bg-canvas text-xs font-medium tabular-nums text-muted ring-1 ring-line">
                      {index + 1}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-muted">
                        <span className="font-medium text-ink">Page {source.page_number}</span>
                        {citationNumber !== undefined && (
                          <span className="rounded bg-accent-soft px-1.5 py-px font-medium text-accent-strong">
                            Cited [{citationNumber}]
                          </span>
                        )}
                      </span>
                      <span className="mt-1 block text-sm leading-snug text-ink break-words">
                        {heading ?? (
                          <span className="line-clamp-1 text-muted">{source.text}</span>
                        )}
                      </span>
                    </span>
                    <ChevronDownIcon className="mt-1 size-4 shrink-0 text-muted transition-transform group-open:rotate-180" />
                  </summary>

                  <div className="border-t border-line px-4 pt-3 pb-4">
                    <p className="text-sm leading-relaxed text-ink break-words whitespace-pre-line">
                      {source.text}
                    </p>
                    <dl className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted">
                      {sectionLabel && (
                        <div className="flex gap-1">
                          <dt>Section:</dt>
                          <dd className="text-ink">{sectionLabel}</dd>
                        </div>
                      )}
                      <div className="flex gap-1">
                        <dt>Retrieval score:</dt>
                        <dd className="tabular-nums text-ink">{source.score.toFixed(3)}</dd>
                      </div>
                      <div className="flex min-w-0 gap-1">
                        <dt>Chunk:</dt>
                        <dd className="truncate font-mono text-ink">{source.chunk_id}</dd>
                      </div>
                    </dl>
                  </div>
                </details>
              </li>
            );
          })}
        </ol>
      )}
    </section>
  );
}
