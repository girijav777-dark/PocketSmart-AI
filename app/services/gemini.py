import time

from google import genai

from ..config import get_settings


settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key
)


def demo_recommendation(prompt: str) -> str:
    """
    Demo recommendation used when Gemini API is unavailable
    or the daily quota has been exhausted.
    """

    return """
HOME RECOMMENDATIONS

Budget:
Based on your selected budget

RECOMMENDED PLAN

1. Item:
   LED Ceiling Light
   Estimated Price: ₹1,500
   Reason:
   Energy-efficient and suitable for modern home interiors.

2. Item:
   Sofa
   Estimated Price: ₹12,000
   Reason:
   Provides comfortable seating while keeping the budget practical.

3. Item:
   TV Unit
   Estimated Price: ₹6,000
   Reason:
   A simple TV unit can improve the organization and appearance
   of the living room.

4. Item:
   Ceiling Fan
   Estimated Price: ₹3,000
   Reason:
   A practical essential item for everyday use.

BUDGET SUMMARY

The recommended items are selected as a sample plan
for demonstration purposes.

IMPORTANT:
This is a DEMO recommendation because the Gemini API
daily quota is currently unavailable.

Once the Gemini quota becomes available again,
PocketSmart AI will generate a personalized AI recommendation.
"""


def generate_recommendation(prompt: str) -> str:

    # Check whether Gemini API key exists
    if not settings.gemini_api_key:
        print("Gemini API key is not configured.")
        return demo_recommendation(prompt)

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
            )

            return response.text or demo_recommendation(prompt)

        except Exception as e:

            error_text = str(e)

            # ==========================================
            # GEMINI DAILY QUOTA EXCEEDED
            # ==========================================

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                # Daily quota exhausted
                if (
                    "GenerateRequestsPerDay" in error_text
                    or "per day" in error_text.lower()
                    or "daily" in error_text.lower()
                ):

                    print()
                    print("=" * 60)
                    print("Gemini daily quota exceeded.")
                    print("Using DEMO recommendation.")
                    print("=" * 60)
                    print()

                    return demo_recommendation(prompt)

                # Temporary rate limit
                if attempt < max_retries - 1:

                    wait_time = 5 * (attempt + 1)

                    print(
                        f"Gemini rate limit reached. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                print("Gemini rate limit still active.")
                print("Using DEMO recommendation.")

                return demo_recommendation(prompt)

            # ==========================================
            # GEMINI TEMPORARILY UNAVAILABLE
            # ==========================================

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < max_retries - 1:

                    wait_time = 3 * (attempt + 1)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                print(
                    "Gemini is unavailable after multiple attempts."
                )

                return demo_recommendation(prompt)

            # ==========================================
            # OTHER GEMINI ERROR
            # ==========================================

            print()
            print("Gemini error:")
            print(error_text)
            print()
            print("Using DEMO recommendation.")

            return demo_recommendation(prompt)

    return demo_recommendation(prompt)