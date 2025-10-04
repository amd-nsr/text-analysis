import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULTS = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "OPENAI_DEFAULT_MODEL": "gpt-4",
    "OPENAI_EMBEDDING_MODEL": "text-embedding-3-large",
    "OPENAI_IMAGE_SIZE": "1024x1024",
    "OPENAI_SPEECH_MODEL": "whisper-1",
    "OPENAI_REQUEST_TIMEOUT": 30,  # seconds
    "OPENAI_MAX_RETRIES": 3,
    "OPENAI_RETRY_WAIT": 2,        # seconds
    "OPENAI_LOG_REQUESTS": True,
}

class OpenAISettings:
    def __getattr__(self, item: str):
        if item in DEFAULTS:
            return os.getenv(item, DEFAULTS[item])
        raise AttributeError(f"Invalid OpenAI setting: {item}")

settings = OpenAISettings()
