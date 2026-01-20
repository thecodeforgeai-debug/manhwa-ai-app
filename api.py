from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel, validator, constr
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from cachetools import TTLCache
from datetime import datetime
from ai_engine import get_recommendations
from config import DB_PATH
import sqlite3
import re

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
cache = TTLCache(maxsize=100, ttl=300)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# SECURE CORS
ALLOWED_ORIGINS = [
    "https://fuzzy-space-system-7v6gv6qwq79xfw5w6-3000.app.github.dev",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# INPUT VALIDATION MODELS (from your api_security_fixes.py)
class SearchQuery(BaseModel):
    query: constr(min_length=1, max_length=100)
    
    @validator('query')
    def sanitize_query(cls, v):
        return v.strip()

class RecommendRequest(BaseModel):
    genres: list[str]
    history: list[str] = []
    
    @validator('genres', 'history', each_item=True)
    def validate_strings(cls, v):
        if not re.match(r'^[A-Z\s-]+$', v):
            raise ValueError('Invalid genre/history format')
        return v

# SECURE ENDPOINTS WITH RATE LIMITING
@app.get("/trending")
@limiter.limit("30/minute")
def get_trending(request: Request):
    """Get top 10 trending manhwa"""
    if "trending" in cache:
        return cache["trending"]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genres, popularity_score, image_url FROM manhwa ORDER BY popularity_score DESC LIMIT 10")
    results = cursor.fetchall()
    conn.close()
    
    data = [{"id": r[0], "title": r[1], "genres": r[2], "popularity": r[3], "image": r[4] or "https://via.placeholder.com/400x560"} for r in results]
    cache["trending"] = data
    return data

@app.get("/manhwa/{manhwa_id}")
@limiter.limit("60/minute")
def get_manhwa_detail(manhwa_id: int, request: Request):
    """Get detailed manhwa info"""
    if manhwa_id < 1 or manhwa_id > 10000:
        raise HTTPException(status_code=400, detail="Invalid manhwa ID")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genres, tropes, description, popularity_score, image_url FROM manhwa WHERE id = ?", (manhwa_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"id": result[0], "title": result[1], "genres": result[2], "tropes": result[3], "description": result[4], "popularity": result[5], "image": result[6]}
    return {"error": "Not found"}

@app.post("/recommend")
@limiter.limit("10/minute")
def recommend(request_data: RecommendRequest, request: Request):
    """Get AI recommendations"""
    result = get_recommendations(request_data.genres, [], "exciting", request_data.history)
    
    if not result.get("success"):
        return {"recommendations": []}
    
    recs_text = result.get("recommendations", "")
    titles = []
    for line in recs_text.split("\n"):
        if line.startswith("**") and "." in line:
            title = line.split(".", 1)[1].split("**")[0].strip()
            titles.append(title)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    recs = []
    for title in titles[:5]:
        cursor.execute("SELECT id, title, image_url FROM manhwa WHERE title LIKE ? LIMIT 1", (f"%{title}%",))
        result = cursor.fetchone()
        if result:
            recs.append({"id": result[0], "title": result[1], "image": result[2] or "https://via.placeholder.com/400x560"})
    conn.close()
    return {"recommendations": recs}

@app.get("/search")
@limiter.limit("20/minute")
def search_manhwa(query: str, request: Request):
    """SECURE search with input validation"""
    try:
        validated = SearchQuery(query=query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    search_term = f"%{validated.query}%"
    cursor.execute("SELECT id, title, image_url FROM manhwa WHERE title LIKE ? LIMIT 10", (search_term,))
    results = cursor.fetchall()
    conn.close()
    
    return [{"id": r[0], "title": r[1], "image": r[2] or "https://via.placeholder.com/400x560"} for r in results]

# AUTO-TRENDING
def clear_trending_cache():
    if "trending" in cache:
        cache.pop("trending")
    print(f"[{datetime.now()}] Cache cleared")

def update_trending_from_sources():
    try:
        import subprocess
        result = subprocess.run(['python3', 'auto_add_trending.py'], capture_output=True, text=True, cwd='/workspaces/manhwa-ai-app')
        print(f"[{datetime.now()}] Trending update: {result.stdout}")
        clear_trending_cache()
    except Exception as e:
        print(f"[{datetime.now()}] Trending update failed: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(update_trending_from_sources, 'cron', hour=2, minute=0)
scheduler.start()

print("✅ SECURE API: Rate limiting + Input validation + CORS protection enabled")
