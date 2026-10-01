from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / "apps" / "api" / ".env")
from app.generation.generator import Generator

def main():
    generator = Generator()

    context = [
        {
            "chunk": {
                "page_number": 34,
                "text": (
                    "5. Referral system for diabetes management. "
                    "Purpose: To assess the availability of referral "
                    "and back-referral systems for clinical services."
                ),
            }
        }
    ]

    question = (
        "What indicator assesses the referral system "
        "for diabetes management?"
    )

    answer = generator.generate(
        query=question,
        context=context,
    )

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()