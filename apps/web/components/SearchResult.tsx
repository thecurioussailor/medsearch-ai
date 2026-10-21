"use client";

import { useId, useMemo, useState } from "react";
import type { AskResponse } from "@/lib/types";
import { AnswerCard, type ResolvedCitation } from "./AnswerCard";
import { SourceList } from "./SourceList";

interface SearchResultProps {
  question: string;
  response: AskResponse;
  onNewSearch: () => void;
}

export function SearchResult({ question, response, onNewSearch }: SearchResultProps) {
  const idPrefix = useId();
  const getItemId = (index: number) => `${idPrefix}-source-${index}`;

  // Start with cited passages expanded so the evidence is visible straight away.
  const { citations, citationNumbers, initiallyOpen } = useMemo(() => {
    const indexByChunk = new Map<string, number>();
    response.sources.forEach((source, index) => {
      if (!indexByChunk.has(source.chunk_id)) indexByChunk.set(source.chunk_id, index);
    });

    const seen = new Set<string>();
    const resolved: ResolvedCitation[] = [];
    for (const citation of response.citations) {
      if (seen.has(citation.chunk_id)) continue;
      seen.add(citation.chunk_id);
      resolved.push({ ...citation, sourceIndex: indexByChunk.get(citation.chunk_id) ?? null });
    }

    return {
      citations: resolved,
      citationNumbers: new Map(resolved.map((c, i) => [c.chunk_id, i + 1])),
      initiallyOpen: new Set(
        resolved.flatMap((c) => (c.sourceIndex === null ? [] : [c.sourceIndex])),
      ),
    };
  }, [response]);

  const [openIndexes, setOpenIndexes] = useState<ReadonlySet<number>>(initiallyOpen);
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  function handleToggle(index: number, open: boolean) {
    setOpenIndexes((current) => {
      if (current.has(index) === open) return current;
      const next = new Set(current);
      if (open) next.add(index);
      else next.delete(index);
      return next;
    });
  }

  function handleCitationSelect(index: number) {
    handleToggle(index, true);
    setActiveIndex(index);

    requestAnimationFrame(() => {
      const item = document.getElementById(getItemId(index));
      if (!item) return;
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      item.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      item.querySelector<HTMLElement>("summary")?.focus({ preventScroll: true });
    });
  }

  return (
    <div className="flex flex-col gap-6">
      <AnswerCard
        question={question}
        answer={response.answer}
        citations={citations}
        onCitationSelect={handleCitationSelect}
        onNewSearch={onNewSearch}
      />
      <SourceList
        sources={response.sources}
        citationNumbers={citationNumbers}
        openIndexes={openIndexes}
        activeIndex={activeIndex}
        onToggle={handleToggle}
        getItemId={getItemId}
      />
    </div>
  );
}
