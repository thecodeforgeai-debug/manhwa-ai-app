import os
import streamlit as st

# Try to get API key from Streamlit secrets
try:
    ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
except Exception as e:
    # If not in secrets, try environment variable
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    if not ANTHROPIC_API_KEY:
        raise ValueError(f"API key not found! Error: {e}")

# Configuration
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024
TEMPERATURE = 1.0
DB_PATH = "data/manhwa.db"
FREE_RECS_PER_DAY = 3
PREMIUM_PRICE = 4.99
APP_TITLE = "Manhwa AI Recommender"
APP_DESCRIPTION = "Get personalized manhwa recommendations powered by AI"
