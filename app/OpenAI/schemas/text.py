from typing import List, Literal
from pydantic import BaseModel, Field


class TextAnalysisSchema(BaseModel):
    """Schema for text analysis response."""
    summary: str = Field(..., description="Concise summary of the input text.")
    sentiment: Literal["positive", "negative", "neutral"] = Field(..., description="Overall sentiment of the text.")
    keywords: List[str] = Field(..., description="List of key topics or phrases from the text.")

