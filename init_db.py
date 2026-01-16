import sqlite3

conn = sqlite3.connect("manhwa.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS manhwa (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    popularity INTEGER
);
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
