import sqlite3

DB_PATH = "data/manhwa.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(manhwa);")
columns = cursor.fetchall()

print("\n📋 Columns in 'manhwa' table:\n")
for col in columns:
    print(f"- {col[1]} ({col[2]})")

conn.close()
