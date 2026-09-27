from .catalog_service import (
    home_catalog,
    party_catalog,
    jewelry_catalog
)

from .gemini_service import GeminiService

from ..schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest,
    RecommendationResponse
)


class RecommendationEngine:

    def __init__(
        self,
        ai_service=None
    ):

        self.ai = (
            ai_service
            or GeminiService()
        )


    def home(
        self,
        data: HomeRequest
    ) -> RecommendationResponse:

        catalog = home_catalog(
            data.style,
            [
                item.model_dump()
                for item in data.items
            ]
        )

        allocation = {

            "Furniture":
                round(data.budget * 0.40, 2),

            "Lighting":
                round(data.budget * 0.15, 2),

            "Decor":
                round(data.budget * 0.15, 2),

            "Storage":
                round(data.budget * 0.15, 2),

            "Contingency":
                round(data.budget * 0.15, 2),
        }

        prompt = f"""
You are PocketSmart AI,
a budget planning assistant.

Create a practical home interior
shopping plan.

Budget:
INR {data.budget}

Style:
{data.style}

Rooms:
{", ".join(data.rooms)}

Requested items:
{", ".join(
    f"{item.quantity} x {item.category}"
    for item in data.items
)}

Use these catalog/search options:

{catalog}

Requirements:

1. Keep the estimated total at or below
   the user's budget.

2. Prefer practical and affordable choices.

3. Do not claim live stock.

4. Do not claim exact live prices.

5. Do not claim live ratings.

6. Do not claim live availability.

7. Use only supplied platform and URL
   values for platform/url.

8. Explain important trade-offs briefly.

9. Return valid JSON matching the
   requested response schema.
"""

        result = self.ai.generate(
            prompt
        )

        return self._sanitize(
            result,
            data.budget,
            catalog,
            allocation,
            "Home Interior Budget Plan"
        )


    def party(
        self,
        data: PartyRequest
    ) -> RecommendationResponse:

        catalog = party_catalog(
            data.event_type,
            data.city
        )

        allocation = {

            "Catering":
                round(data.budget * 0.45, 2),

            "Venue":
                round(data.budget * 0.20, 2),

            "Decoration":
                round(data.budget * 0.15, 2),

            "Entertainment":
                round(data.budget * 0.10, 2),

            "Contingency":
                round(data.budget * 0.10, 2),
        }

        prompt = f"""
You are PocketSmart AI,
a party budget planning assistant.

Budget:
INR {data.budget}

Guests:
{data.guests}

Event type:
{data.event_type}

Venue:
{data.venue}

City:
{data.city}

Catalog/search layer:

{catalog}

Create a realistic,
budget-safe party plan.

Scale catering suggestions
according to guest count.

Do not claim live availability.

Do not claim exact current prices.

Use supplied URLs only.

Return valid JSON matching
the response schema.
"""

        result = self.ai.generate(
            prompt
        )

        return self._sanitize(
            result,
            data.budget,
            catalog,
            allocation,
            f"{data.event_type.title()} Party Budget Plan"
        )


    def jewelry(
        self,
        data: JewelryRequest,
        image_bytes=None,
        mime_type=None
    ) -> RecommendationResponse:

        catalog = jewelry_catalog(
            data.style,
            data.occasion,
            data.metal_preference
        )

        allocation = {

            "Primary piece":
                round(data.budget * 0.50, 2),

            "Secondary piece":
                round(data.budget * 0.25, 2),

            "Optional set/accessory":
                round(data.budget * 0.15, 2),

            "Contingency":
                round(data.budget * 0.10, 2),
        }

        if image_bytes:

            image_note = (
                "An outfit image is supplied. "
                "Use it only for visible color "
                "and style coordination."
            )

        else:

            image_note = (
                "No outfit image was supplied."
            )

        prompt = f"""
You are PocketSmart AI,
a jewelry budget and styling assistant.

Budget:
INR {data.budget}

Occasion:
{data.occasion}

Style:
{data.style}

Outfit color:
{data.outfit_color or "not specified"}

Metal preference:
{data.metal_preference or "not specified"}

{image_note}

Catalog/search layer:

{catalog}

If an image is supplied,
describe only visible style
and color cues relevant to
jewelry coordination.

Do not identify the person.

Do not infer sensitive personal traits.

Do not claim live availability.

Do not claim exact current prices.

Use supplied URLs only.

Return valid JSON matching
the response schema.
"""

        result = self.ai.generate(
            prompt,
            image_bytes=image_bytes,
            mime_type=mime_type
        )

        return self._sanitize(
            result,
            data.budget,
            catalog,
            allocation,
            "Jewelry Budget Plan"
        )


    @staticmethod
    def _sanitize(
        result,
        budget,
        catalog,
        allocation,
        title
    ):

        result.budget = budget

        result.title = title

        result.allocations = allocation

        if result.estimated_total > budget:

            result.recommendations = sorted(
                result.recommendations,
                key=lambda item:
                    item.estimated_price
                    * item.quantity
            )

            total = 0.0

            kept = []

            for item in result.recommendations:

                cost = (
                    item.estimated_price
                    * item.quantity
                )

                if total + cost <= budget:

                    kept.append(item)

                    total += cost

            result.recommendations = kept

            result.estimated_total = round(
                total,
                2
            )

        result.savings = round(
            max(
                budget -
                result.estimated_total,
                0
            ),
            2
        )

        result.disclaimer = (
            "Prices and links are search-oriented "
            "estimates. Verify the retailer page "
            "for current price, taxes, delivery, "
            "stock, and availability before "
            "purchasing."
        )

        return result