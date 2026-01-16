import sqlite3

conn = sqlite3.connect("manhwa.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM manhwa")
print("Total rows in manhwa:", cursor.fetchone()[0])

cursor.execute("SELECT title FROM manhwa LIMIT 5")
print("Sample titles:")
for row in cursor.fetchall():
    print("-", row[0])

conn.close()
