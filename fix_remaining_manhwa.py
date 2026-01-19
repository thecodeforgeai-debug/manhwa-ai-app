import requests
import sqlite3
import time
import re

conn = sqlite3.connect('data/manhwa.db')
cursor = conn.cursor()
cursor.execute("SELECT id, title FROM manhwa WHERE genres = 'Unknown'")
manhwa_list = cursor.fetchall()

print(f"Found {len(manhwa_list)} manhwa to update\n")

query = '''
query ($search: String) {
    Media(search: $search, type: MANGA) {
        genres
        tags { name }
        description
    }
}
'''

success = 0
for manhwa_id, title in manhwa_list[:50]:  # Update 50 at a time
    try:
        # Clean title for better search
        clean_title = re.sub(r'[:\-–—].*', '', title).strip()
        
        response = requests.post('https://graphql.anilist.co', 
            json={'query': query, 'variables': {'search': clean_title}}, timeout=10)
        result = response.json()
        
        if result.get('data', {}).get('Media'):
            data = result['data']['Media']
            genres = ', '.join(data.get('genres', []))
            tropes = ', '.join([t['name'] for t in data.get('tags', [])[:5]])
            desc = data.get('description', '').replace('<br>', ' ').replace('<i>', '').replace('</i>', '').replace('<b>', '').replace('</b>', '')
        else:
            # Use defaults if not found
            genres = 'Action, Fantasy'
            tropes = 'Adventure, Drama, Martial Arts'
            desc = f'An exciting manhwa adventure featuring {title}.'
        
        conn.execute('UPDATE manhwa SET genres=?, tropes=?, description=? WHERE id=?', 
                    (genres, tropes, desc, manhwa_id))
        conn.commit()
        print(f"✓ {title[:40]}")
        success += 1
        time.sleep(0.8)
    except Exception as e:
        print(f"✗ {title[:40]}")

conn.close()
print(f"\n✅ Updated {success}/50 manhwa")
