import type { Source } from "./types";

/** "indicator_definition" -> "Indicator definition" */
export function formatSectionType(value: string | null): string | null {
  if (!value) return null;
  const words = value.replace(/[_-]+/g, " ").trim();
  if (!words) return null;
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** Short heading for a source passage, built only from fields the API returned. */
export function describeSource(source: Source): string | null {
  const { indicator_number: number, indicator_name: name } = source;
  if (number != null && name) return `Indicator ${number} · ${name}`;
  if (number != null) return `Indicator ${number}`;
  if (name) return name;
  return formatSectionType(source.section_type);
}
