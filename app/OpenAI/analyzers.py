from .schemas.text import TextAnalysisSchema
from .prompts.text import TextAnalysisPrompt
from .services.response import ResponseService

class TextAnalyzer:
    """
    AI-powered review analyzer using the ResponseService with structured outputs.
    """

    def __init__(self, schema=None, prompt=None):
        self.schema = schema or TextAnalysisSchema
        self.prompt = prompt or TextAnalysisPrompt()
        self.response_service = ResponseService()

    def analyze(self, text: str) -> TextAnalysisSchema:
        """
        Run the text through the AI model and parse into schema.
        """
        prompt_text = self.prompt.build(text)

        analysis_data = self.response_service.parse_response(
            input_text=prompt_text,
            schema_model=self.schema,   # Pydantic schema passed directly
            temperature=0.2,
        )

        return analysis_data  # Already parsed into TextAnalysisSchema instance
    