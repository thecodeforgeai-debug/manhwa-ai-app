import sqlite3
import json
from typing import List, Dict, Optional
from config import DB_PATH

def init_database():
    """Initialize the manhwa database with tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manhwa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genres TEXT NOT NULL,
            tropes TEXT NOT NULL,
            description TEXT,
            popularity_score INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            genres_searched TEXT,
            tropes_searched TEXT,
            recommended_titles TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def populate_sample_data():
    """Populate database with sample manhwa data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sample_manhwa = [
        ("Who Made Me a Princess", "isekai,romance,fantasy", "reincarnation,royalty,second-chance",
         "A woman is reborn as princess Athanasia, who was destined to be killed by her father.", 95),

        ("The Villainess Reverses the Hourglass", "isekai,romance,revenge", "time-travel,villainess,redemption",
         "Aria goes back in time with an hourglass and uses it to change her fate.", 92),

        ("Inso's Law", "romance,comedy,school-life", "found-family,friendship,slice-of-life",
         "Dan-I suddenly finds herself in a romance novel as a side character.", 88),

        ("Your Throne", "drama,psychological,fantasy", "revenge,strong-female-lead,body-swap",
         "Medea and Psyche swap bodies and must navigate their situations.", 94),

        ("The Remarried Empress", "romance,drama,historical", "divorce,remarriage,empress,political-intrigue",
         "Empress Navier is replaced by a younger woman and must navigate her new life.", 96),

        ("Beware of the Villainess!", "comedy,romance,isekai", "villainess,strong-female-lead,reverse-harem",
         "Melissa is reborn as the villainess and decides to avoid the original plot.", 90),

        ("The Way to Protect the Female Lead's Older Brother", "romance,fantasy,isekai", "obsessive-love,reincarnation,tragedy-prevention",
         "Roxana must survive in a family of villains while protecting the male lead.", 91),

        ("Kill the Villainess", "drama,fantasy,isekai", "villainess,tragedy,dark-themes",
         "Eris wants to return to her original world and will do anything to escape.", 89),

        ("A Stepmother's Märchen", "drama,fantasy,isekai", "time-loop,stepmother,family-dynamics",
         "Shuli is stuck in a time loop trying to be a good stepmother.", 93),

        ("I'm the Queen in This Life", "romance,historical,drama", "reincarnation,revenge,political-intrigue",
         "Ariadne is reborn and uses her knowledge to take revenge.", 87),
    ]

    cursor.execute("SELECT COUNT(*) FROM manhwa")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany('''
            INSERT INTO manhwa (title, genres, tropes, description, popularity_score)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_manhwa)
        conn.commit()
        print(f"Added {len(sample_manhwa)} manhwa to database!")
    else:
        print(f"Database already contains {count} manhwa entries.")

    conn.close()

def search_manhwa(genres=None, tropes=None, limit=10):
    """Search manhwa by genres and/or tropes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM manhwa WHERE 1=1"
    params = []

    if genres:
        genre_conditions = " OR ".join(["genres LIKE ?" for _ in genres])
        query += f" AND ({genre_conditions})"
        params.extend([f"%{g}%" for g in genres])

    if tropes:
        trope_conditions = " OR ".join(["tropes LIKE ?" for _ in tropes])
        query += f" AND ({trope_conditions})"
        params.extend([f"%{t}%" for t in tropes])

    query += " ORDER BY popularity_score DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    manhwa_list = []
    for row in results:
        manhwa_list.append({
            'id': row[0],
            'title': row[1],
            'genres': row[2].split(','),
            'tropes': row[3].split(','),
            'description': row[4],
            'popularity_score': row[5]
        })

    return manhwa_list

def save_user_history(user_id, genres, tropes, recommendations):
    """Save user search history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO user_history (user_id, genres_searched, tropes_searched, recommended_titles)
        VALUES (?, ?, ?, ?)
    ''', (user_id, genres, tropes, json.dumps(recommendations)))

    conn.commit()
    conn.close()

def get_user_history(user_id, limit=5):
    """Get user's search history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT genres_searched, tropes_searched, recommended_titles, timestamp
        FROM user_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, limit))

    results = cursor.fetchall()
    conn.close()

    history = []
    for row in results:
        history.append({
            'genres': row[0],
            'tropes': row[1],
            'recommendations': json.loads(row[2]),
            'timestamp': row[3]
        })

    return history

if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    init_database()
    populate_sample_data()
    print("Database setup complete!")
