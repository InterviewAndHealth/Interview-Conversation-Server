import os
from dotenv import load_dotenv

load_dotenv(override=True)

PORT = int(os.getenv("PORT", 8002))

REDIS_URL = os.getenv("REDIS_URL")

INTERVIEW_DURATION = int(os.getenv("INTERVIEW_DURATION", 30))

MODEL = os.getenv("MODEL", "llama3.1")

USE_GROQ = os.getenv("USE_GROQ", "false").lower() == "true"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

_important_variable = [REDIS_URL, INTERVIEW_DURATION]

for var in _important_variable:
    if var is None:
        raise ValueError(f"Missing environment variable: {var}")
