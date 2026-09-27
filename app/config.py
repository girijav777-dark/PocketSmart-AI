import os
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


class Settings:
    app_name: str = os.getenv("APP_NAME", "PocketSmart AI")

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    ).strip()

    jwt_secret: str = os.getenv(
        "JWT_SECRET",
        "dev-only-change-me"
    )

    database_path: str = os.getenv(
        "DATABASE_PATH",
        "data/pocketsmart.db"
    )

    max_image_mb: int = int(
        os.getenv("MAX_IMAGE_MB", "5")
    )

    cookie_secure: bool = (
        os.getenv("COOKIE_SECURE", "false").lower()
        == "true"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()