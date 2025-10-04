from openai import OpenAI
from pydantic import BaseModel
from .base import OpenAIBaseService
from ..core.conf import settings


class TextService(OpenAIBaseService):
    """Text completion service with structured output support."""

    def __init__(self, model="text-davinci-003"):
        super().__init__()
        self.model = model
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def complete(self, input_text: str, parse_json=True, **kwargs):
        """
        Perform a text completion request using the legacy Completions API.

        Args:
            prompt (str): Input text prompt.
            parse_json (bool): If True, attempt to parse the response as JSON.
            kwargs: Extra OpenAI API parameters.

        Returns:
            str | dict: Raw text or parsed JSON.
        """
        payload = {
            "model": self.model,
            "prompt": input_text,
            **kwargs,
        }
        response = self.request(self.client.completions.create, **payload)

        raw_content = self._extract_content(response, is_chat=False)
        return self._parse_json(raw_content) if parse_json else raw_content

    def parse_complete(self, prompt: str, schema_model: type[BaseModel], **kwargs):
        """
        Perform a text completion request and return structured output
        validated by a Pydantic model.

        Args:
            prompt (str): Input text prompt.
            schema_model (BaseModel subclass): Pydantic model for structured parsing.
            kwargs: Extra OpenAI API parameters.

        Returns:
            BaseModel: Parsed structured output.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "text_format": schema_model,
            **kwargs,
        }
        response = self.request(self.client.completions.parse, **payload)
        return response.output_parsed
