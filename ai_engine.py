import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE

def get_claude_client():
    """Initialize and return Anthropic client with API key"""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        return client
    except Exception as e:
        raise Exception(f"Failed to initialize Anthropic client: {str(e)}")

def get_recommendations(genres, tropes, mood, user_history=None):
    try:
        client = get_claude_client()
        
        prompt = f"""You are a manhwa recommendation expert. Based on the following preferences, recommend 3 manhwa titles with brief descriptions.

Genres: {', '.join(genres)}
Tropes: {', '.join(tropes)}
Mood/Vibe: {mood}

Format your response as:

**1. [Title]**
*Genres: [genres]*
[2-3 sentence description]

**2. [Title]**
*Genres: [genres]*
[2-3 sentence description]

**3. [Title]**
*Genres: [genres]*
[2-3 sentence description]"""

        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        raise Exception(f"Error getting recommendations: {str(e)}")

def analyze_tropes(manhwa_summary):
    try:
        client = get_claude_client()
        
        prompt = f"""Analyze this manhwa summary and identify the main tropes present.

Summary: {manhwa_summary}

List 3-5 tropes and explain how they appear."""

        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        raise Exception(f"Error analyzing tropes: {str(e)}")
