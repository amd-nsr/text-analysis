from .base import BasePrompt

class TextAnalysisPrompt(BasePrompt):
    def build(self, text: str) -> str:
        return f"""
You are a text analyzer. Analyze the following text:

Review: "{text}"
"""
    