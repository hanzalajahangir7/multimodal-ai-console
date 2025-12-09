from openai import AsyncOpenAI
from src.config import config

aclient = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
