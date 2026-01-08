import anthropic
from typing import List, Dict, Optional
import json
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE

def get_claude_client():
    """Initialize and return Claude client."""
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_api_key_here":
        raise ValueError("Please set your ANTHROPIC_API_KEY in the .env file!")
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def get_recommendations(genres, tropes, mood, db_results, user_history=None):
    """Get personalized manhwa recommendations using Claude AI."""
    client = get_claude_client()

    db_context = "\n".join([
        f"- {m['title']}: {m['description']} (Genres: {', '.join(m['genres'])}, Tropes: {', '.join(m['tropes'])})"
        for m in db_results[:15]
    ])

    history_context = ""
    if user_history:
        recent_recs = [h['recommendations'] for h in user_history[:3]]
        history_context = f"\n\nUser's recent preferences: {json.dumps(recent_recs, indent=2)}"

    system_prompt = f"""You are an expert manhwa recommender with deep knowledge of Korean webcomics.
Your role is to provide personalized, enthusiastic recommendations that match users' preferences perfectly.

Focus on:
1. Matching the requested genres, tropes, and mood
2. Explaining WHY each recommendation fits
3. Being specific about plot elements and character dynamics
4. Ranking recommendations from best to least fitting
5. If database matches are limited, suggest similar popular manhwa you know{history_context}"""

    user_prompt = f"""The user wants manhwa recommendations with these preferences:
- Genres: {genres}
- Tropes: {tropes}
- Mood: {mood}

Here are potential matches from our database:
{db_context if db_context else "No exact matches found in database."}

Please provide:
1. Your top 5 recommendations (mix database matches and your knowledge)
2. For each: title, brief description (2-3 sentences), why it matches their preferences
3. A "bonus pick" if you know something perfect they might love

Format as a structured response with clear sections."""

    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        response_text = message.content[0].text

        return {
            'success': True,
            'recommendations': response_text,
            'source': 'claude_ai'
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'recommendations': 'Unable to generate recommendations at this time.'
        }

def analyze_tropes(summary):
    """Analyze a manhwa summary to identify tropes, genres, and find similar titles."""
    client = get_claude_client()

    system_prompt = """You are a manhwa analyst specializing in identifying tropes, themes, and genres.
You can identify subtle narrative patterns, character archetypes, and story structures common in manhwa.

Provide detailed, insightful analysis that helps users understand the story's core elements."""

    user_prompt = f"""Analyze this manhwa summary and provide:

Summary to analyze:
"{summary}"

Please provide:
1. **Primary Genres** (2-4 genres, e.g., romance, isekai, fantasy)
2. **Key Tropes** (4-6 specific tropes with brief explanations)
3. **Character Archetypes** (main character types present)
4. **Mood/Tone** (overall vibe of the story)
5. **Similar Manhwa** (3-4 titles with reasoning why they're similar)
6. **What Makes It Unique** (distinctive elements)

Be specific and insightful!"""

    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        response_text = message.content[0].text

        return {
            'success': True,
            'analysis': response_text,
            'source': 'claude_ai'
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'analysis': 'Unable to analyze at this time.'
        }

def test_api_connection():
    """Test if Claude API is working."""
    try:
        client = get_claude_client()
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=100,
            messages=[{"role": "user", "content": "Say 'API Connected!' if you can read this."}]
        )
        return True, message.content[0].text
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    success, message = test_api_connection()
    if success:
        print(f"✅ API Test Successful: {message}")
    else:
        print(f"❌ API Test Failed: {message}")
