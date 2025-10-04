from openai import OpenAI
import openai
from pydantic import BaseModel
from .base import OpenAIBaseService
from ..core.conf import settings


class ChatService(OpenAIBaseService):
    """ChatCompletion service with structured output support."""

    def __init__(self, model="gpt-4"):
        super().__init__()
        self.model = model
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def chat(self, messages, parse_json=True, **kwargs):
        """
        Perform a chat request using the Chat Completions API.

        Args:
            messages (list[dict]): List of role-content messages.
            parse_json (bool): If True, attempt to parse the response as JSON.
            kwargs: Extra OpenAI API parameters.

        Returns:
            str | dict: Raw text or parsed JSON.
        """

        payload = {
            "model": self.model, 
            "messages": messages,
            **kwargs
        }
        response = self.request(self.client.chat.completions.create, **payload)

        raw_content = self._extract_content(response, is_chat=True)
        return self._parse_json(raw_content) if parse_json else raw_content

    def parse_chat(
            self, 
            messages, 
            schema_model: type[BaseModel], 
            **kwargs
    ):
        """
        Perform a chat request and return structured output
        validated by a Pydantic model.

        Args:
            messages (list[dict]): List of role-content messages.
            schema (BaseModel subclass): Pydantic model for structured parsing.
            kwargs: Extra OpenAI API parameters.

        Returns:
            BaseModel: Parsed structured output.
        """
        payload = {
            "model": self.model, 
            "messages": messages,
            "text_format": schema_model,
            **kwargs
        }
        response = self.request(self.client.chat.completions.parse, **payload)
        return response.output_parsed
