from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


PlannerType = Literal[
    "home",
    "party",
    "jewelry"
]


class RegisterRequest(BaseModel):
    email: str

    password: str = Field(
        min_length=8,
        max_length=128
    )

    full_name: str = Field(
        min_length=2,
        max_length=80
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:

        value = value.strip().lower()

        if "@" not in value:
            raise ValueError(
                "Enter a valid email address."
            )

        domain = value.split("@")[-1]

        if "." not in domain:
            raise ValueError(
                "Enter a valid email address."
            )

        return value


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HomeItem(BaseModel):
    category: str = Field(
        min_length=2,
        max_length=80
    )

    quantity: int = Field(
        ge=1,
        le=50
    )


class HomeRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    style: str = Field(
        default="modern",
        min_length=2,
        max_length=80
    )

    rooms: list[str] = Field(
        min_length=1,
        max_length=10
    )

    items: list[HomeItem] = Field(
        min_length=1,
        max_length=30
    )


class PartyRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        ge=1,
        le=5000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        min_length=2,
        max_length=120
    )

    city: str = Field(
        default="Bengaluru",
        min_length=2,
        max_length=80
    )


class RecommendationItem(BaseModel):
    name: str
    category: str

    estimated_price: float = Field(
        ge=0
    )

    quantity: int = Field(
        ge=1
    )

    platform: str

    url: str

    reason: str

    within_budget: bool


class RecommendationResponse(BaseModel):
    title: str

    summary: str

    budget: float

    estimated_total: float = Field(
        ge=0
    )

    savings: float

    allocations: dict[str, float]

    recommendations: list[
        RecommendationItem
    ]

    tips: list[str]

    disclaimer: str


class JewelryRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        min_length=2,
        max_length=80
    )

    outfit_color: Optional[str] = Field(
        default=None,
        max_length=80
    )

    metal_preference: Optional[str] = Field(
        default=None,
        max_length=80
    )