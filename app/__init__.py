import os
from dotenv import load_dotenv

load_dotenv(override=True)

PORT = int(os.getenv("PORT", 8002))

REDIS_URL = os.getenv("REDIS_URL")

INTERVIEW_DURATION = int(os.getenv("INTERVIEW_DURATION", 30))

MODEL = os.getenv("MODEL", "llama3.1")

_important_variable = [REDIS_URL, INTERVIEW_DURATION]

for var in _important_variable:
    if var is None:
        raise ValueError(f"Missing environment variable: {var}")
