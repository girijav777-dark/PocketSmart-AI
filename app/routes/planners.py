from typing import Optional

from fastapi import (
    APIRouter,
    Form,
    UploadFile,
    File,
    HTTPException,
)

from ..services.gemini import generate_recommendation


router = APIRouter()


# =========================================================
# HOME PLANNER
# =========================================================

@router.post("/generate-home")
async def generate_home(
    budget: float = Form(...),
    home_style: str = Form(...),
    rooms: str = Form(...),
    items: str = Form(...),
    additional_requirements: str = Form(""),
):
    """
    Generate a personalized home interior plan.

    The frontend sends:
        budget
        home_style
        rooms
        items
        additional_requirements
    """

    prompt = f"""
You are PocketSmart AI, a budget-aware home planning assistant.

Create a practical and personalized home interior recommendation
based on the user's requirements.

USER REQUIREMENTS
-----------------

Budget: ₹{budget:,.0f}

Home Style: {home_style}

Rooms:
{rooms}

Items Needed:
{items}

Additional Requirements:
{additional_requirements if additional_requirements else "None provided"}

IMPORTANT REQUIREMENTS
----------------------

1. Stay within the user's total budget.
2. Do not exceed the budget.
3. Prioritize essential items first.
4. Consider the selected home style.
5. Consider all selected rooms.
6. Consider the quantity of each requested item.
7. Give realistic estimated prices in Indian Rupees.
8. Explain briefly why each recommendation is suitable.
9. If the requested items are too expensive for the budget,
   suggest practical alternatives.
10. Keep the response easy to understand.
11. Clearly separate recommendations by room where possible.
12. Consider the user's additional requirements.

Return the answer in this format:

HOME RECOMMENDATIONS

BUDGET:
₹amount

STYLE:
selected style

ROOMS:
selected rooms

RECOMMENDED PLAN

1. Item:
   Room:
   Quantity:
   Estimated Price:
   Reason:

2. Item:
   Room:
   Quantity:
   Estimated Price:
   Reason:

3. Item:
   Room:
   Quantity:
   Estimated Price:
   Reason:

BUDGET SUMMARY

TOTAL ESTIMATED COST:
₹amount

REMAINING BUDGET:
₹amount

ADDITIONAL TIPS

- Tip 1
- Tip 2
- Tip 3
"""

    try:

        ai_result = generate_recommendation(prompt)

        return {
            "success": True,
            "planner_type": "home",

            "data": {
                "planner_type": "home",
                "budget": budget,
                "style": home_style,
                "home_style": home_style,
                "rooms": rooms,
                "items": items,
                "additional_requirements": additional_requirements,
                "recommendations": ai_result,
            },
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {str(e)}",
        )


# =========================================================
# PARTY PLANNER
# =========================================================

@router.post("/generate-party")
async def generate_party(
    budget: float = Form(...),
    guests: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(...),
    city: str = Form(...),
):
    prompt = f"""
You are PocketSmart AI, a budget-aware party planning assistant.

Create a practical party plan using:

Budget: ₹{budget:,.0f}
Number of Guests: {guests}
Event Type: {event_type}
Venue: {venue}
City: {city}

Requirements:
- Stay within the given budget.
- Consider the number of guests.
- Suggest practical food, decoration, venue-related
  and entertainment expenses.
- Give realistic estimated prices in Indian Rupees.
- Prioritize important expenses.
- Do not exceed the total budget.
- Keep the recommendations easy to understand.

Return the answer in this format:

PARTY PLAN

1. Category:
   Estimated Cost:
   Details:

2. Category:
   Estimated Cost:
   Details:

3. Category:
   Estimated Cost:
   Details:

TOTAL ESTIMATED COST:
₹amount

REMAINING BUDGET:
₹amount
"""

    try:

        ai_result = generate_recommendation(prompt)

        return {
            "success": True,
            "planner_type": "party",

            "data": {
                "planner_type": "party",
                "budget": budget,
                "guests": guests,
                "event_type": event_type,
                "venue": venue,
                "city": city,
                "recommendations": ai_result,
            },
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {str(e)}",
        )


# =========================================================
# JEWELRY PLANNER
# =========================================================

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_color: str = Form(""),
    metal_preference: str = Form(""),
    outfit_image: Optional[UploadFile] = File(None),
):
    image_name = None

    if outfit_image:
        image_name = outfit_image.filename

    prompt = f"""
You are PocketSmart AI, a budget-aware jewelry recommendation assistant.

Create practical jewelry recommendations using:

Budget: ₹{budget:,.0f}
Occasion: {occasion}
Style: {style}
Outfit Color: {outfit_color}
Metal Preference: {metal_preference}

Requirements:
- Stay within the given budget.
- Consider the occasion.
- Consider the requested style.
- Consider the outfit color when provided.
- Consider the preferred metal when provided.
- Suggest realistic jewelry options.
- Give estimated prices in Indian Rupees.
- Prioritize suitable options within the budget.
- Do not exceed the total budget.

Return the answer in this format:

JEWELRY RECOMMENDATIONS

1. Jewelry:
   Estimated Price:
   Metal:
   Why it suits the user:

2. Jewelry:
   Estimated Price:
   Metal:
   Why it suits the user:

3. Jewelry:
   Estimated Price:
   Metal:
   Why it suits the user:

TOTAL ESTIMATED COST:
₹amount

REMAINING BUDGET:
₹amount
"""

    try:

        ai_result = generate_recommendation(prompt)

        return {
            "success": True,
            "planner_type": "jewelry",

            "data": {
                "planner_type": "jewelry",
                "budget": budget,
                "occasion": occasion,
                "style": style,
                "outfit_color": outfit_color,
                "metal_preference": metal_preference,
                "outfit_image": image_name,
                "recommendations": ai_result,
            },
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {str(e)}",
        )


# =========================================================
# DETAILED RECOMMENDATIONS
# =========================================================

@router.post("/recommendations-details")
async def recommendations_details(
    category: str = Form(...),
    budget: float = Form(...),
    preferences: str = Form(...),
):
    category = category.lower().strip()

    if category not in ["home", "party", "jewelry"]:

        raise HTTPException(
            status_code=400,
            detail="Category must be home, party, or jewelry",
        )

    prompt = f"""
You are PocketSmart AI, a detailed budget-based recommendation assistant.

Generate detailed product recommendations based on:

Category: {category}
Budget: ₹{budget:,.0f}
User Preferences: {preferences}

Requirements:
- Stay within the user's budget.
- Recommend practical and relevant options.
- Give estimated prices in Indian Rupees.
- Explain why each recommendation is suitable.
- Prioritize important items.
- Do not exceed the total budget.
- Provide multiple options where possible.

Return the answer in this format:

DETAILED RECOMMENDATIONS

Category:
{category}

Budget:
₹{budget:,.0f}

1. Product/Item:
   Estimated Price:
   Why Recommended:

2. Product/Item:
   Estimated Price:
   Why Recommended:

3. Product/Item:
   Estimated Price:
   Why Recommended:

TOTAL ESTIMATED COST:
₹amount

REMAINING BUDGET:
₹amount
"""

    try:

        ai_result = generate_recommendation(prompt)

        return {
            "success": True,
            "category": category,
            "budget": budget,
            "preferences": preferences,
            "recommendations": ai_result,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {str(e)}",
        )