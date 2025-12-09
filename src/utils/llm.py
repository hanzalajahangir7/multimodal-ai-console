from openai import AsyncOpenAI
from src.config import config

def get_aclient():
    """Lazy initialization of OpenAI client"""
    if not config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return AsyncOpenAI(api_key=config.OPENAI_API_KEY)

aclient = None  # Will be initialized on first use
