import Link from "next/link";
import { KNOWLEDGE_SOURCE } from "@/lib/constants";
import { DocumentIcon, LogoMark } from "./icons";

export function Header() {
  return (
    <header className="border-b border-line bg-surface">
      <div className="mx-auto flex h-14 w-full max-w-5xl items-center justify-between gap-3 px-4 sm:h-16 sm:px-6">
        <Link
          href="/"
          className="flex min-w-0 items-center gap-3 rounded-md focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-accent"
        >
          <LogoMark className="size-8 shrink-0" />
          <span className="flex min-w-0 flex-col leading-tight">
            <span className="text-[15px] font-semibold tracking-tight text-ink">
              MedSearch AI
            </span>
            <span className="hidden truncate text-xs text-muted sm:block">
              Evidence-grounded medical research
            </span>
          </span>
        </Link>

        <p
          className="flex shrink-0 items-center gap-2 rounded-full border border-line bg-canvas px-3 py-1.5 text-xs text-muted"
          title={`Knowledge source: ${KNOWLEDGE_SOURCE.publisher} ${KNOWLEDGE_SOURCE.title}`}
        >
          <span className="size-1.5 rounded-full bg-accent" aria-hidden="true" />
          <span className="sr-only">Knowledge source:</span>
          <DocumentIcon className="hidden size-3.5 sm:block" />
          <span>
            <span className="font-medium text-ink">{KNOWLEDGE_SOURCE.publisher}</span>
            <span className="hidden sm:inline"> · {KNOWLEDGE_SOURCE.title}</span>
          </span>
        </p>
      </div>
    </header>
  );
}
