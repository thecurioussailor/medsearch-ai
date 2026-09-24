import re

def clean_text(text: str) -> str:
    # Remove Unicode replacement characters caused by
    # unsupported/misdecoded PDF glyphs.
    text = text.replace("\ufffd", " ")

    # Remove ASCII control characters except normal whitespace.
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)

    # Collapse repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text