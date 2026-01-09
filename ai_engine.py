import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE

def get_recommendations(genres, tropes, mood, user_history=None):
    """Get manhwa recommendations from Claude"""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        prompt = f"""You are a manhwa recommendation expert. Based on the following preferences, recommend 3 manhwa titles with brief descriptions.

Genres: {', '.join(genres)}
Tropes: {', '.join(tropes)}
Mood/Vibe: {mood}

{f'Previously recommended (avoid these): {", ".join(user_history)}' if user_history else ''}

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
        
        recommendations_text = message.content[0].text
        
        # Return as a dictionary for main.py
        return {
            'success': True,
            'recommendations': recommendations_text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def analyze_tropes(manhwa_summary):
    """Analyze a manhwa summary and identify tropes"""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        prompt = f"""Analyze this manhwa summary and identify the main tropes present.

Summary: {manhwa_summary}

List 3-5 tropes and explain how they appear."""

        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            'success': True,
            'analysis': message.content[0].text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
