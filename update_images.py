import sqlite3

images = {
    "The Remarried Empress": "https://i.imgur.com/bCYq6hV.jpg",
    "Who Made Me a Princess": "https://i.imgur.com/jJ5RCLN.jpg",
    "Your Throne": "https://i.imgur.com/4kCE38C.jpg",
    "A Stepmother's Märchen": "https://i.imgur.com/PVI2zIV.jpg",
    "The Villainess Reverses the Hourglass": "https://i.imgur.com/L1g3NKg.jpg",
    "The Way to Protect the Female Lead's Older Brother": "https://i.imgur.com/edPpq8A.jpg",
    "Beware of the Villainess!": "https://i.imgur.com/gRW1Ha1.jpg",
    "Kill the Villainess": "https://i.imgur.com/lHKsMyJ.jpg",
    "Inso's Law": "https://i.imgur.com/J88e1Hs.jpg",
    "I'm the Queen in This Life": "https://i.imgur.com/ypoXQDl.jpg"
}

conn = sqlite3.connect('data/manhwa.db')
cursor = conn.cursor()

for title, url in images.items():
    cursor.execute("UPDATE manhwa SET image_url = ? WHERE title = ?", (url, title))
    print(f"✓ Updated: {title}")

conn.commit()
conn.close()
print("\n✓ All images updated!")