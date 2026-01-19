from fastapi import FastAPI
from ai_engine import get_recommendations
import sqlite3
from config import DB_PATH

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/trending")
def get_trending():
    """Get top 10 trending manhwa"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genres, popularity_score, image_url FROM manhwa ORDER BY popularity_score DESC LIMIT 10")
    results = cursor.fetchall()
    return [{"id": r[0], "title": r[1], "genres": r[2], "popularity": r[3], "image": r[4] or "https://via.placeholder.com/400x560"} for r in results]


@app.get("/manhwa/{manhwa_id}")
def get_manhwa_detail(manhwa_id: int):
    """Get detailed manhwa info"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genres, tropes, description, popularity_score, image_url FROM manhwa WHERE id = ?", (manhwa_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"id": result[0], "title": result[1], "genres": result[2], "tropes": result[3], "description": result[4], "popularity": result[5], "image": result[6]}
    return {"error": "Not found"}
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
@app.get("/search")
def search_manhwa(query: str):
    """Search manhwa by title"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, image_url FROM manhwa WHERE " + " OR ".join(["title LIKE ?" for _ in query.split()]) + " LIMIT 10", tuple(f"%{word}%" for word in query.split()))
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "image": r[2] or f"https://picsum.photos/seed/{r[0]}/400/560"} for r in results]
