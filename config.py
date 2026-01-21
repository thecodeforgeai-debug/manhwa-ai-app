import os

# Get API key from environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Configuration
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024
TEMPERATURE = 1.0
DB_PATH = "manhwa.db"
FREE_RECS_PER_DAY = 3
PREMIUM_PRICE = 4.99
APP_TITLE = "Manhwa AI Recommender"
APP_DESCRIPTION = "Get personalized manhwa recommendations powered by AI"
