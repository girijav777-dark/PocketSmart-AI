from typing import Optional

from google import genai
from google.genai import types

from ..config import get_settings
from ..schemas import RecommendationResponse


class GeminiService:

    def __init__(self):

        self.settings = get_settings()

        if self.settings.gemini_api_key:

            self.client = genai.Client(
                api_key=self.settings.gemini_api_key
            )

        else:

            self.client = None


    def _require_client(self):

        if not self.client:

            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Copy .env.example to .env and add "
                "your Google AI Studio API key."
            )


    def generate(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None
    ) -> RecommendationResponse:

        self._require_client()

        contents = [
            prompt
        ]

        if image_bytes:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type or "image/jpeg"
                )
            )

        response = self.client.models.generate_content(

            model=self.settings.gemini_model,

            contents=contents,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                response_schema=
                    RecommendationResponse,
            )
        )

        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return RecommendationResponse.model_validate_json(
            response.text
        )