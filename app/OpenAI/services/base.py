import time
import logging
import json
import re
from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    BadRequestError,
    AuthenticationError,
    RateLimitError,
)
from ..core.conf import settings

logger = logging.getLogger(__name__)


def _clean_json_string(raw: str) -> str:
    """Remove Markdown fences and extra formatting around JSON."""
    # Strip triple backticks and optional language hints like ```json
    cleaned = re.sub(r"^```(json)?\s*|\s*```$", "", raw.strip(), flags=re.DOTALL)
    return cleaned.strip()


class OpenAIBaseService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def request(self, func, *args, **kwargs):
        """Generic wrapper with retries, error handling, and logging."""
        for attempt in range(settings.OPENAI_MAX_RETRIES):
            try:
                response = func(
                    *args,
                    # request_timeout=settings.OPENAI_REQUEST_TIMEOUT,
                    **kwargs,
                )
                if settings.OPENAI_LOG_REQUESTS:
                    logger.info(f"[OpenAI] {func.__name__} success")
                return response

            except (APIError, APIConnectionError, BadRequestError,
                    AuthenticationError, RateLimitError) as e:
                logger.warning(
                    f"[OpenAI] {func.__name__} failed (attempt {attempt+1}): {e}"
                )
                time.sleep(settings.OPENAI_RETRY_WAIT)

        raise Exception("OpenAI request failed after retries")

    def _extract_content(self, response, is_chat: bool = True) -> str:
        """
        Extract raw text from OpenAI response (chat, text, or responses API).
        For new `responses.create`, you can use response.output_text directly.
        """
        try:
            if hasattr(response, "output_text"):  # new unified API
                return response.output_text.strip()
            elif is_chat:  # legacy chat completion
                return response.choices[0].message["content"]
            else:  # legacy text completion
                return response.choices[0].text.strip()
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"[OpenAI] Failed to extract content: {e}")
            return ""

    def _parse_json(self, raw_content: str) -> dict:
        """Try to parse JSON output safely, even if wrapped in markdown."""
        if not raw_content:
            return {"error": "Empty response"}

        cleaned = _clean_json_string(raw_content)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning(f"[OpenAI] Invalid JSON output: {raw_content}")
            return {"error": "Invalid JSON", "raw": raw_content}
    