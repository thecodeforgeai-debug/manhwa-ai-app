import sqlite3

DB_PATH = "data/manhwa.db"

def get_top10_trending():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, popularity_score
        FROM manhwa
        ORDER BY popularity_score DESC
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    top10 = get_top10_trending()

    print("\n🔥 REAL TOP 10 TRENDING TODAY 🔥\n")
    for i, (title, score) in enumerate(top10, 1):
        print(f"{i}. {title} — Popularity: {score}")
    print("\n===============================\n")
