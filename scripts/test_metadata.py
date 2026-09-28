from app.ingestion.metadata import get_indicator_metadata
from app.ingestion.metadata import (
    get_indicator_for_page,
    get_indicator_metadata,
)

def main():
    for indicator_number in range(1, 13):
        metadata = get_indicator_metadata(indicator_number)

        print(
            f"{metadata['indicator_number']:>2} | "
            f"{metadata['subdomain']:<35} | "
            f"{metadata['indicator_name']}"
        )


if __name__ == "__main__":
    main()

print("\nPAGE MAPPING")
print("=" * 60)

for page_number in range(30, 42):
    indicator_number = get_indicator_for_page(page_number)

    metadata = get_indicator_metadata(indicator_number)

    print(
        f"Page {page_number:>2} → "
        f"Indicator {indicator_number:>2} → "
        f"{metadata['subdomain']} → "
        f"{metadata['indicator_name']}"
    )