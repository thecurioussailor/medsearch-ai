import { KNOWLEDGE_SOURCE } from "@/lib/constants";
import { InfoIcon } from "./icons";

export function Disclaimer() {
  return (
    <aside
      aria-label="About these answers"
      className="flex gap-3 rounded-xl border border-line bg-surface/60 px-4 py-3 text-xs leading-relaxed text-muted"
    >
      <InfoIcon className="mt-px size-4 shrink-0" />
      <p>
        Answers are based only on the {KNOWLEDGE_SOURCE.publisher}{" "}
        {KNOWLEDGE_SOURCE.title.toLowerCase()} document and link to the passages
        they draw on. MedSearch AI is a research aid, not a substitute for
        professional medical advice.
      </p>
    </aside>
  );
}
