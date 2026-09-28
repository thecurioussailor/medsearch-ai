import re

from app.ingestion.loader import load_pdf


PDF_PATH = "data/raw/diabetes_monitoring_guidance.pdf"


def main():
    pages = load_pdf(PDF_PATH)

    heading_pattern = re.compile(
        r"^(\d+)\.\s+(.+)$",
        re.MULTILINE,
    )

    for page in pages:
        text = page["text"]

        matches = list(heading_pattern.finditer(text))

        for index, match in enumerate(matches):
            number = int(match.group(1))
            name = match.group(2).strip()

            start = match.end()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(text)

            section = text[start:end]

            if "Indicator name" not in section:
                continue

            print(
                f"Page {page['page_number']:>2} | "
                f"Indicator {number:>2} | "
                f"{name}"
            )


if __name__ == "__main__":
    main()