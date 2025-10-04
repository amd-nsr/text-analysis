from abc import ABC, abstractmethod

class BasePrompt(ABC):
    """Base class for pluggable prompts."""

    @abstractmethod
    def build(self, text: str) -> str:
        """Builds the structured prompt from input text."""
        pass
