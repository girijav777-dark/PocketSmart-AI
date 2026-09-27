import os
from pathlib import Path
import tempfile


TEST_DB = (
    Path(tempfile.gettempdir())
    / "pocketsmart_test.db"
)


if TEST_DB.exists():
    TEST_DB.unlink()


os.environ["DATABASE_PATH"] = str(
    TEST_DB
)

os.environ["JWT_SECRET"] = (
    "test-secret"
)

os.environ["GEMINI_API_KEY"] = ""


from fastapi.testclient import TestClient

from app.main import app

from app.routes.planners import (
    engine
)

from app.schemas import (
    RecommendationResponse,
    RecommendationItem
)


class FakeAI:

    def generate(
        self,
        prompt,
        image_bytes=None,
        mime_type=None
    ):

        return RecommendationResponse(

            title="Test Plan",

            summary=
                "A test recommendation.",

            budget=10000,

            estimated_total=1200,

            savings=8800,

            allocations={
                "Test":
                    10000
            },

            recommendations=[

                RecommendationItem(

                    name=
                        "Test Item",

                    category=
                        "Test",

                    estimated_price=
                        1200,

                    quantity=
                        1,

                    platform=
                        "Amazon",

                    url=
                        "https://www.amazon.in/s?k=test",

                    reason=
                        "Test reason",

                    within_budget=
                        True
                )
            ],

            tips=[
                "Test tip"
            ],

            disclaimer=
                "Test disclaimer"
        )


engine.ai = FakeAI()


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_login_and_home():

    email = (
        "test@example.com"
    )

    response = client.post(

        "/register",

        json={

            "email":
                email,

            "full_name":
                "Test User",

            "password":
                "password123"
        }
    )

    assert response.status_code == 200


    response = client.post(

        "/login",

        json={

            "email":
                email,

            "password":
                "password123"
        }
    )

    assert response.status_code == 200


    response = client.get(
        "/api/session-info"
    )

    assert response.status_code == 200

    assert (
        response.json()["email"]
        == email
    )


    response = client.post(

        "/api/generate-home",

        json={

            "budget":
                10000,

            "style":
                "modern",

            "rooms": [
                "Living Room"
            ],

            "items": [

                {
                    "category":
                        "Lighting",

                    "quantity":
                        1
                }
            ]
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["estimated_total"]
        <= 10000
    )


def test_party_validation():

    response = client.post(

        "/api/generate-party",

        json={

            "budget":
                -1,

            "guests":
                10,

            "event_type":
                "Birthday",

            "venue":
                "Home",

            "city":
                "Bengaluru"
        }
    )

    assert response.status_code == 422


def test_jewelry_multipart():

    response = client.post(

        "/api/generate-jewelry",

        data={

            "budget":
                "10000",

            "occasion":
                "Wedding",

            "style":
                "Elegant",

            "outfit_color":
                "Blue",

            "metal_preference":
                "Silver"
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["title"]
        == "Jewelry Budget Plan"
    )