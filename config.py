import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024
TEMPERATURE = 0.7
DB_PATH = "data/manhwa.db"
FREE_RECS_PER_DAY = 3
PREMIUM_PRICE = 4.99
