from fastapi import FastAPI
from ai_engine import get_recommendations
import sqlite3
from config import DB_PATH

app = FastAPI()

@app.get("/trending")
def get_trending():
    """Get top 10 trending manhwa"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, image_url FROM manhwa ORDER BY popularity_score DESC LIMIT 10")
    results = cursor.fetchall()
    conn.close()
    return [{"title": r[0], "image": r[1] or f"https://picsum.photos/seed/{r[0]}/400/560"} for r in results]

@app.post("/recommend")
def recommend(request: dict):
    genres = request.get("genres", [])
    # mood removed
    history = request.get("history", [])
    result = get_recommendations(genres, [], "exciting", history)
    
    if not result.get('success'):
        return {"recommendations": []}
    
    # Parse the AI text response
    recs_text = result.get('recommendations', '')
    titles = []
    for line in recs_text.split('\n'):
        if line.startswith('**') and '.' in line:
            title = line.split('.', 1)[1].split('**')[0].strip()
            titles.append(title)
    
    return {"recommendations": [{"title": t} for t in titles[:3]]}