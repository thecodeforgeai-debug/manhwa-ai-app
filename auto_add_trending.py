#!/usr/bin/env python3
import requests
import sqlite3
import time
from datetime import datetime

DB_PATH = "data/manhwa.db"

def get_existing_titles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM manhwa")
    existing = {row[0].lower().strip() for row in cursor.fetchall()}
    conn.close()
    return existing

def fetch_anilist_trending():
    """Fetch trending from Anilist API"""
    query = '''
    query {
        Page(page: 1, perPage: 50) {
            media(type: MANGA, format: MANGA, sort: TRENDING_DESC, countryOfOrigin: "KR") {
                title { english romaji }
                popularity
                favourites
                averageScore
            }
        }
    }
    '''
    try:
        response = requests.post('https://graphql.anilist.co', json={'query': query}, timeout=10)
        data = response.json()
        results = []
        for item in data['data']['Page']['media']:
            title = item['title']['english'] or item['title']['romaji']
            score = (item['popularity'] or 0) + (item['favourites'] or 0) * 2 + (item['averageScore'] or 0) * 10
            results.append((title, int(score)))
        return results
    except Exception as e:
        print(f"❌ Anilist error: {e}")
        return []

def fetch_mal_trending():
    """Fetch trending from MyAnimeList (via Jikan API)"""
    try:
        response = requests.get('https://api.jikan.moe/v4/manga?type=manhwa&order_by=popularity&limit=50', timeout=10)
        data = response.json()
        results = []
        for item in data.get('data', []):
            title = item['title']
            score = (item.get('members', 0) + item.get('favorites', 0) * 2 + (item.get('score', 0) or 0) * 1000)
            results.append((title, int(score)))
        time.sleep(1)  # Rate limit
        return results
    except Exception as e:
        print(f"❌ MAL error: {e}")
        return []

def fetch_mangadex_trending():
    """Fetch popular from MangaDex"""
    try:
        params = {
            'limit': 50,
            'contentRating[]': ['safe', 'suggestive'],
            'order[followedCount]': 'desc',
            'originalLanguage[]': 'ko'
        }
        response = requests.get('https://api.mangadex.org/manga', params=params, timeout=10)
        data = response.json()
        results = []
        for item in data.get('data', []):
            title = item['attributes']['title'].get('en') or list(item['attributes']['title'].values())[0]
            # MangaDex doesn't return follows in list, so use static score
            results.append((title, 1000))
        return results
    except Exception as e:
        print(f"❌ MangaDex error: {e}")
        return []

def aggregate_trending():
    """Combine all sources and rank"""
    print("🔍 Fetching from multiple sources...")
    
    all_results = {}
    
    # Fetch from all sources
    for title, score in fetch_anilist_trending():
        all_results[title.lower()] = all_results.get(title.lower(), {'title': title, 'score': 0})
        all_results[title.lower()]['score'] += score
    
    for title, score in fetch_mal_trending():
        all_results[title.lower()] = all_results.get(title.lower(), {'title': title, 'score': 0})
        all_results[title.lower()]['score'] += score
    
    for title, score in fetch_mangadex_trending():
        all_results[title.lower()] = all_results.get(title.lower(), {'title': title, 'score': 0})
        all_results[title.lower()]['score'] += score
    
    # Sort by combined score
    sorted_results = sorted(all_results.values(), key=lambda x: x['score'], reverse=True)
    
    return [(item['title'], item['score']) for item in sorted_results[:20]]

def add_new_manhwa(titles_scores):
    """Add new manhwa to database"""
    existing = get_existing_titles()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    for title, score in titles_scores:
        if title.lower() not in existing:
            cursor.execute(
                "INSERT INTO manhwa (title, genres, tropes, popularity_score) VALUES (?, ?, ?, ?)",
                (title, "Unknown", "Unknown", score)
            )
            added += 1
            print(f"✅ Added: {title} (score: {score})")
    
    conn.commit()
    conn.close()
    return added

def main():
    print("=" * 70)
    print("🤖 MULTI-SOURCE TRENDING MANHWA UPDATER")
    print("=" * 70)
    
    trending = aggregate_trending()
    print(f"📊 Found {len(trending)} trending titles")
    
    added = add_new_manhwa(trending)
    print(f"\n✅ Added {added} new manhwa")
    print(f"📚 Update complete!")

if __name__ == "__main__":
    main()