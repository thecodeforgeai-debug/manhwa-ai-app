import requests
import sqlite3
import time

conn = sqlite3.connect('data/manhwa.db')
cursor = conn.cursor()
cursor.execute("SELECT id, title FROM manhwa")
manhwa_list = cursor.fetchall()

query = '''
query ($search: String) {
    Media(search: $search, type: MANGA, format: MANGA) {
        genres
        tags { name }
        description
    }
}
'''

success = 0
failed = 0

for manhwa_id, title in manhwa_list:
    try:
        response = requests.post('https://graphql.anilist.co', 
            json={'query': query, 'variables': {'search': title}}, timeout=10)
        result = response.json()
        
        if 'data' not in result or result['data']['Media'] is None:
            print(f"Not found: {title}")
            failed += 1
            continue
            
        data = result['data']['Media']
        genres = ', '.join(data.get('genres', [])) or 'Action, Fantasy'
        tropes = ', '.join([t['name'] for t in data.get('tags', [])[:5]]) or 'Adventure, Drama'
        desc = data.get('description', '').replace('<br>', ' ').replace('<i>', '').replace('</i>', '') or 'An epic manhwa story.'
        
        conn.execute('UPDATE manhwa SET genres=?, tropes=?, description=? WHERE id=?', 
                    (genres, tropes, desc, manhwa_id))
        conn.commit()
        print(f"✓ {title}")
        success += 1
        time.sleep(1)
    except Exception as e:
        print(f"Error: {title}")
        failed += 1

conn.close()
print(f"\nDone! Success: {success}, Failed: {failed}")
