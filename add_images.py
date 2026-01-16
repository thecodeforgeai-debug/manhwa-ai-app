import sqlite3

# Real manhwa cover URLs (you can change these)
images = {
    "The Remarried Empress": "https://i.imgur.com/8xYvZ5K.jpg",
    "Who Made Me a Princess": "https://i.imgur.com/9LqJ5tN.jpg",
    "Your Throne": "https://i.imgur.com/3wXKj7L.jpg",
    "A Stepmother's Märchen": "https://i.imgur.com/5xRqP8M.jpg",
    "The Villainess Reverses the Hourglass": "https://i.imgur.com/7KqYvN2.jpg",
}

conn = sqlite3.connect('data/manhwa.db')
cursor = conn.cursor()

for title, url in images.items():
    cursor.execute("UPDATE manhwa SET image_url = ? WHERE title = ?", (url, title))
    print(f"Updated: {title}")

conn.commit()
conn.close()
print("Done!")