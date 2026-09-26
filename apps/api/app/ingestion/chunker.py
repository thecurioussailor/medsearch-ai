import re

def split_into_paragraphs(text: str) -> list[str]:
    """
    Split document text into paragraph-like blocks.
    """
    paragraphs = re.split(r"\n\s*\n", text)

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]

def chunk_text(
    text:str,
    chunk_size: int = 2000,
    overlap: int = 400
) -> list[str]:
    """
    Create chunks while trying to preserve paragraph and word boundaries.
    """

    if not text.strip():
        return []

    paragraphs = split_into_paragraphs(text)

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If adding this paragraph keeps us within the target size,
        # add it to the current chunk.
        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
            current_chunk = (
                f"{current_chunk}\n\n{paragraph}"
                if current_chunk
                else paragraph
            )
            continue

        # Save the current chunk before starting a new one.
        if current_chunk:
            chunks.append(current_chunk.strip())

        # If the paragraph itself is too large,
        # split it safely by words.
        if len(paragraph) > chunk_size:
            words = paragraph.split()

            current_chunk = ""

            for word in words:
                candidate = (
                    f"{current_chunk} {word}"
                    if current_chunk
                    else word
                )

                if len(candidate) <= chunk_size:
                    current_chunk = candidate
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())

                    current_chunk = word

        else:
            current_chunk = paragraph

    # Add remaining text.
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Add overlap between chunks.
    if overlap <= 0 or len(chunks) <= 1:
        return chunks

    overlapped_chunks = [chunks[0]]

    for i in range(1, len(chunks)):
        previous = chunks[i - 1]

        overlap_text = previous[-overlap:]

        # Move the overlap back to a word boundary.
        space_index = overlap_text.find(" ")

        if space_index != -1:
            overlap_text = overlap_text[space_index + 1:]

        chunk = f"{overlap_text} {chunks[i]}".strip()

        overlapped_chunks.append(chunk)

    return overlapped_chunks

def create_chunks(
    pages: list[dict],
    document_id: str,
    chunk_size: int = 2000,
    overlap: int = 400,
) -> list[dict]:
    """
    Create metadata-rich chunks from extracted PDF pages.
    """

    chunk_id = 0

    chunks = []

    for page in pages:
        if not page["has_text"]:
            continue

        page_chunks = chunk_text(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_index, text in enumerate(page_chunks):
            chunks.append(
                {
                    "chunk_id": f"{document_id}-{chunk_id:06d}",
                    "document_id": document_id,
                    "page_number": page["page_number"],
                    "chunk_index": chunk_index,
                    "text": text,
                }
            )
            
            chunk_id += 1

    return chunks