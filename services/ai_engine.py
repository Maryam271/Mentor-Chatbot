import logging
import time
from google import genai
from backend.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger("ai_engine")

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Model fallback chain: try the configured model first, then these in order
# if it 404s / becomes unavailable. Keeps the app alive across Google's
# model deprecations without needing a redeploy.
_FALLBACK_MODELS = ["gemini-flash-latest", "gemini-2.0-flash"]


class AIServiceError(Exception):
    """Raised when the LLM cannot produce a usable response."""


def _candidate_models() -> list[str]:
    """Configured model first, then fallbacks, de-duplicated, order preserved."""
    seen = set()
    ordered = []
    for name in [GEMINI_MODEL, *_FALLBACK_MODELS]:
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def get_ai_response(prompt: str, files: list | None = None, max_retries: int = 2) -> str:
    """
    Call the Gemini LLM with the given prompt and return the generated text.

    Tries the configured model, and if it fails with a non-transient error
    (e.g. 404 - model retired), moves to the next candidate model. Within
    each model, retries a couple of times on transient failures (timeouts,
    temporary 5xx/429s). If every model/attempt fails, raises
    AIServiceError with the real underlying error logged — never falls
    back to a canned response.
    """
    if not GEMINI_API_KEY or _client is None:
        raise AIServiceError(
            "GEMINI_API_KEY is not configured on the server. "
            "Set a valid key in the .env file."
        )

    last_error: Exception | None = None

    for model_name in _candidate_models():
        for attempt in range(1, max_retries + 1):
            try:
                contents = [prompt]
                if files:
                    import base64
                    from google.genai import types
                    for f in files:
                        file_data = base64.b64decode(f.data)
                        contents.append(
                            types.Part.from_bytes(data=file_data, mime_type=f.mime_type)
                        )

                response = _client.models.generate_content(
                    model=model_name,
                    contents=contents,
                )

                text = (getattr(response, "text", None) or "").strip()
                if not text:
                    raise AIServiceError("Gemini returned an empty response")

                if model_name != GEMINI_MODEL:
                    logger.warning(
                        "Configured model '%s' unavailable; served response using fallback '%s'",
                        GEMINI_MODEL, model_name,
                    )

                return text

            except AIServiceError:
                raise
            except Exception as e:  # noqa: BLE001 - deliberately broad: SDK/network errors
                last_error = e
                logger.error(
                    "Gemini call failed [model=%s, attempt %d/%d]: %s",
                    model_name, attempt, max_retries, e, exc_info=True
                )
                # Model not found/retired -> no point retrying this model, move to next.
                if "404" in str(e) or "NOT_FOUND" in str(e):
                    break
                if attempt < max_retries:
                    time.sleep(1.5 * attempt)  # simple linear backoff before retrying
                    continue

    raise AIServiceError(
        f"AI service unavailable after trying models {_candidate_models()}: {last_error}"
    )