from openai import OpenAI
from pydantic import BaseModel, ValidationError
from typing import Type, Optional, Tuple, Any, Dict

from ..core.conf import settings
from .base import OpenAIBaseService  # assuming your base class is in base.py


class ResponseService(OpenAIBaseService):
    """Unified OpenAI Responses API service with structured output support."""

    def __init__(self, model: str = "gpt-4.1-mini"):
        super().__init__()
        self.model = model
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def response(self, input_text: str, **kwargs) -> str | Dict[str, Any]:
        """
        Perform a general-purpose request using the new Responses API.

        Args:
            input_text (str): Prompt or message input.
            kwargs: Extra parameters passed to OpenAI.

        Returns:
            str | dict: Text output or parsed JSON if valid.
        """
        payload = {
            "model": self.model,
            "input": input_text,
            **kwargs,
        }

        raw_response = self.request(self.client.responses.create, **payload)
        raw_content = self._extract_content(raw_response, is_chat=True)
        return self._parse_json(raw_content) if raw_content else raw_content

    def parse_response(
        self,
        input_text: str,
        schema_model: Type[BaseModel],
        **kwargs,
    ) -> Tuple[Optional[BaseModel], dict]:
        """
        Perform a structured output request using Responses API with Pydantic parsing.

        Args:
            system_message (str): System prompt.
            user_message (str): User input.
            schema_model (BaseModel subclass): Pydantic schema for validation.
            kwargs: Extra parameters passed to OpenAI.

        Returns:
            (BaseModel | None, dict): Validated object or None + raw/parsed metadata.
        """
        payload = {
            "model": self.model,
            "input": input_text,
            "text_format": schema_model,
            **kwargs,
        }

        response = self.request(
            self.client.responses.parse,
            **payload,
        )
        return response.output_parsed
