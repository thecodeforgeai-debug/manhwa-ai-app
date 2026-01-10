#!/usr/bin/env python3
import requests
import sqlite3
import time
from datetime import datetime

DB_PATH = "data/manhwa.db"

# Blacklist generic/junk words
BLACKLIST = {
    'title', 'meme', 'spoiler', 'recommendation', 'sauce', 'source',
    'help', 'question', 'discussion', 'manga', 'manhwa', 'manhua',
    'nsfw', 'spoilers', 'read', 'chapter', 'new', 'best', 'top'
}

def get_existing_titles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM manhwa")
    # Store both original and lowercase for better matching
    existing = {row[0].lower().strip() for row in cursor.fetchall()}
    conn.close()
    return existing

def is_valid_title(title):
    """Check if title is valid (not generic junk)"""
    title_lower = title.lower().strip()
    
    # Too short or too long
    if len(title) < 4 or len(title) > 80:
        return False
    
    # Contains blacklisted words only
    words = set(title_lower.split())
    if words.issubset(BLACKLIST):
        return False
    
    # Is just a single generic word
    if title_lower in BLACKLIST:
        return False
    
    # Contains numbers only or URLs
    if title.replace(' ', '').isdigit() or 'http' in title_lower:
        return False
    
    return True

def search_reddit_for_manhwa():
    print("🔍 Searching Reddit r/manhwa...")
    discovered = {}
    
    try:
        url = "https://www.reddit.com/r/manhwa/hot.json?limit=50"
        headers = {'User-Agent': 'ManhwaRecommender/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                title = post_data.get('title', '')
                selftext = post_data.get('selftext', '')
                score = post_data.get('score', 0)
                
                import re
                patterns = [
                    r'\[(.*?)\]',
                    r'"(.*?)"',
                    r'«(.*?)»',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, title + " " + selftext)
                    for match in matches:
                        match = match.strip()
                        if is_valid_title(match):
                            discovered[match] = discovered.get(match, 0) + score
        
        time.sleep(1)
    except Exception as e:
        print(f"⚠️ Reddit error: {e}")
    
    return discovered

def add_new_manhwa(title):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO manhwa (title, genres, tropes, description)
            VALUES (?, ?, ?, ?)
        """, (title, "action,fantasy", "trending", f"Trending: {title}"))
        
        cursor.execute("""
            INSERT INTO trending_scores (title, recommendation_count, daily_score)
            VALUES (?, 0, 50)
        """, (title,))
        
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def main():
    print("=" * 70)
    print("🤖 AUTO-ADD TRENDING MANHWA (v2 - Smart Filter)")
    print("=" * 70)
    
    existing = get_existing_titles()
    print(f"📚 Database: {len(existing)} manhwa\n")
    
    discovered = search_reddit_for_manhwa()
    print(f"🔍 Discovered: {len(discovered)} mentions\n")
    
    # Filter: valid + not existing + good score
    new_manhwa = []
    for title, score in sorted(discovered.items(), key=lambda x: x[1], reverse=True):
        if title.lower().strip() not in existing and score > 20:  # Higher threshold
            new_manhwa.append((title, score))
    
    print(f"✨ NEW valid manhwa: {len(new_manhwa)}\n")
    
    added = 0
    for title, score in new_manhwa[:5]:  # Limit to top 5
        print(f"  Adding: {title} (score: {score})")
        if add_new_manhwa(title):
            added += 1
            print(f"    ✓ Added")
        else:
            print(f"    ⊘ Duplicate")
    
    print(f"\n✅ Added {added} new manhwa")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM manhwa")
    total = cursor.fetchone()[0]
    conn.close()
    print(f"📚 Total now: {total} manhwa")

if __name__ == "__main__":
    main()
