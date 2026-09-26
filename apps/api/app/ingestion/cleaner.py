import re

def clean_text(text: str) -> str:
    # Remove Unicode replacement characters.
    text = text.replace("\ufffd", " ")

    # Remove control characters except normal whitespace/newlines.
    text = re.sub(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
        " ",
        text,
    )

    # Normalize spaces and tabs, but preserve newlines.
    text = re.sub(r"[^\S\n]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()