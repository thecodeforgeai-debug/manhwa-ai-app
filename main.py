import streamlit as st
import urllib.parse
import requests
import sqlite3
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """Retry decorator for API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def safe_db_query(query_func):
    """Safe database query wrapper"""
    try:
        return query_func()
    except sqlite3.Error as e:
        st.error("❌ Database error. Please refresh the page.")
        return None

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MANHWA INTEL",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# CYBER SEOUL CSS + PARTICLES
# ===============================
st.markdown("""
<style>
    /* Cyber buttons matching search bar */
    .stButton > button {
        background: linear-gradient(45deg, rgba(0,255,255,0.2), rgba(255,0,255,0.2)) !important;
        border: 2px solid #00ffff !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0,255,255,0.5) !important;
        color: #00ffff !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(0,255,255,0.4), rgba(255,0,255,0.4)) !important;
        box-shadow: 0 0 25px rgba(0,255,255,0.8) !important;
        transform: translateY(-2px) !important;
    }
/* --- SAME CSS YOU PROVIDED, UNCHANGED --- */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%) !important;
    font-family: 'Rajdhani', 'Segoe UI', sans-serif !important;
    color: #e0e0ff !important;
}

h1 {
    font-size: 48px !important;
    font-weight: 900 !important;
    text-align: center !important;
    background: linear-gradient(45deg, #00ffff, #ff00ff, #00ffff) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: glitch 3s infinite, neonPulse 2s infinite !important;
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.7) !important;
}

h2 {
    color: #00ffff !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    border-left: 4px solid #ff00ff !important;
    padding-left: 15px !important;
}

.cyber-card {
    background: rgba(10, 10, 26, 0.8) !important;
    border: 2px solid;
    border-image: linear-gradient(45deg, #00ffff, #ff00ff) 1;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    transition: 0.3s ease;
}

.cyber-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 25px rgba(0,255,255,0.5);
}

.rank-badge {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(45deg, #ff00ff, #00ffff);
    color: #0a0a1a;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
}

img {
    width: 100%;
    border-radius: 8px;
    transition: 0.3s ease;
}

img:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(0,255,255,0.6);
}

#MainMenu, footer, header {visibility: hidden;}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

.particle {
    position: fixed;
    background: rgba(0, 255, 255, 0.3);
    border-radius: 50%;
    pointer-events: none;
    animation: float 3s infinite ease-in-out; 
}            

div[data-testid="column"]:has(input[aria-label=""]) {
    max-width: 200px !important;
}           

</style>
           
<script>
for(let i=0; i<20; i++) {
    let p = document.createElement('div');
    p.className = 'particle';
    p.style.width = Math.random()*10+5+'px';
    p.style.height = p.style.width;
    p.style.left = Math.random()*100+'%';
    p.style.top = Math.random()*100+'%';
    p.style.animationDelay = Math.random()*3+'s';
    document.body.appendChild(p);
}
</script>
""", unsafe_allow_html=True)

# ===============================
# HELPERS
# ===============================
@retry_on_failure(max_retries=3, delay=2)
def fetch_anilist_details(title):
    """Fetch manhwa details from Anilist API (excluding adult content)"""
    query = """
    query ($search: String) {
        Media(search: $search, type: MANGA, format: MANGA) {
            title { english romaji }
            description
            genres
            tags { name }
            coverImage { extraLarge }
            isAdult
        }
    }
    """
    try:
        response = requests.post("https://graphql.anilist.co", 
            json={"query": query, "variables": {"search": title}}, timeout=10)
        data = response.json()["data"]["Media"]
        if data.get("isAdult", False):
            return None
        return {
            "description": data.get("description", "").replace("<br>", " ").replace("<i>", "").replace("</i>", ""),
            "genres": ", ".join(data.get("genres", [])),
            "tropes": ", ".join([t["name"] for t in data.get("tags", [])[:5]]),
            "image": data.get("coverImage", {}).get("extraLarge")
        }
    except:
        return None


def show_detail_page(manhwa_id):
    """Display detailed manhwa page"""
    conn = sqlite3.connect("data/manhwa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM manhwa WHERE id = ?", (manhwa_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        st.error("Manhwa not found")
        return
    
    _, title, genres, tropes, desc, pop, img = result
    
    # Fetch from Anilist if data is missing
    if not desc or genres == "Unknown":
        anilist_data = fetch_anilist_details(title)
        if anilist_data:
            if not img:
                img = anilist_data.get("image")
            desc = anilist_data["description"] or desc
            genres = anilist_data["genres"] or genres
            tropes = anilist_data["tropes"] or tropes
    
    # Back button
    if st.button("← BACK TO NEURAL HUB"):
        st.query_params.clear()
        st.rerun()
    
    # Detail layout
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""<a href="{google_search(title)}" target="_blank"><img src="{img or "https://via.placeholder.com/400x560"}" style="width:100%; border-radius:8px;"></a>""", unsafe_allow_html=True)
    with col1:
        if st.button("🔍 Search on Google", key="google_btn", use_container_width=True):
            st.markdown(f"""<script>window.open("{google_search(title)}", "_blank");</script>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<a href="{google_search(title)}" target="_blank" style="text-decoration:none;"><h1 style="color:#00ffff;">{title}</h1></a>""", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#ff00ff;'>⭐ Popularity: {pop}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Genres:</strong> {genres}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Tropes:</strong> {tropes}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{desc or 'No description available.'}</p>", unsafe_allow_html=True)


def google_search(title: str):
    return f"https://www.google.com/search?q={urllib.parse.quote(title + ' manhwa')}"

# ===============================
# MAIN APP
# ===============================
def main():
    # Check if viewing detail page
    if "id" in st.query_params:
        manhwa_id = st.query_params["id"]
        show_detail_page(int(manhwa_id))
        return


 # Header with search in top right
    header_left, header_right = st.columns([6, 1])
    with header_left:
     st.markdown("<h1>MANHWA INTEL</h1>", unsafe_allow_html=True)
    with header_right:
        st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
        st.markdown("""<style>
        div[data-baseweb="input"] > div {
            background: linear-gradient(45deg, rgba(0,255,255,0.2), rgba(255,0,255,0.2)) !important;
            border: 2px solid #00ffff !important;
            border-radius: 8px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.5) !important;
        }
        div[data-baseweb="input"] input {
            color: #00ffff !important;
            font-weight: bold !important;
        }
        </style>""", unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="🔍 Search...", label_visibility="collapsed", key="search")

    # Search results
    if search_query:
        st.markdown(f"<h3 style='color:#00ffff; text-align:center; margin:20px 0;'>Search: {search_query}</h3>", unsafe_allow_html=True)
        try:
            response = requests.get(f"https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/search?query={search_query}", timeout=5)
            search_results = response.json()
            if search_results:
                cols = st.columns(5)
                for i, item in enumerate(search_results[:5]):
                    with cols[i]:
                        st.markdown(f"""<div class="cyber-card" style="padding:10px; height:300px;">
                            <img src="{item['image']}" style="width:100%; height:220px; object-fit:cover;">
                            <p style="font-size:11px; margin-top:5px;">{item['title']}</p>
                        </div>""", unsafe_allow_html=True)
            else:
                st.warning("No results found")
        except Exception as e:
            st.error(f"Search error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1])

    # ===============================
    # LEFT — TRENDING
    # ===============================
    with col_left:
        st.markdown("<h2>𓊝 TRENDING DISTRICT</h2>", unsafe_allow_html=True)

        # Fetch trending from API with retry
        trending = []
        try:
            for attempt in range(3):
                try:
                    response = requests.get("https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/trending", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        trending = [(item["id"], item["title"], item["image"]) for item in data]
                        break
                    time.sleep(2)
                except requests.exceptions.Timeout:
                    if attempt == 2:
                        st.warning("⚠️ Loading trending data is taking longer than usual. Please refresh the page.")
                except requests.exceptions.ConnectionError:
                    if attempt == 2:
                        st.error("❌ Cannot connect to server. Please check your internet connection.")
        except Exception as e:
            st.error(f"❌ Error loading trending: Please try refreshing the page.")

        # Create 2 rows of 5 manhwa each
        row1 = st.columns(5, gap="small")
        row2 = st.columns(5, gap="small")
        
        for i, (manhwa_id, title, img) in enumerate(trending[:10]):
            link = google_search(title)
            col = row1[i] if i < 5 else row2[i - 5]
            
            with col:
                st.markdown(f"""
                <div class="cyber-card" style="padding:10px; height:350px;">
                    <div class="rank-badge" style="position:absolute; top:10px; left:10px; width:28px; height:28px; font-size:14px;">{i+1}</div>
                    <a href="?id={manhwa_id}" style="cursor:pointer;">
                        <img src="{img}" style="width:100%; height:250px; object-fit:cover;">
                    </a>
                    <p style="margin-top:8px; font-size:11px; line-height:1.3; overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">{title}</p>
                </div>
                """, unsafe_allow_html=True)
    # RIGHT — NEURAL INTERFACE
    # ===============================
    with col_right:
        st.markdown("<h2>𓊝 NEURAL INTERFACE</h2>", unsafe_allow_html=True)

        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ffff; margin-top: 0;'>GENRES</h3>", unsafe_allow_html=True)
        genres = st.multiselect(
            "Genres",
            ["ACTION", "FANTASY", "ROMANCE", "THRILLER", "CYBERPUNK", "MYSTERY"],
            default=[],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Initialize recommendation history
        if 'rec_history' not in st.session_state:
            st.session_state.rec_history = []
        
        # Tropes Selector
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ffff; margin-top: 0;'>TROPES</h3>", unsafe_allow_html=True)
        tropes = st.multiselect(
            "Select narrative patterns",
            ["SYSTEM", "REINCARNATION", "CYBER-ENHANCEMENT", "TIME TRAVEL", "DUNGEON CRAWL", "APOCALYPSE"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("𓊝 INITIATE NEURAL SCAN"):
            st.session_state.scan = True

        if st.session_state.get("scan", False):     
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)

            with st.spinner('🔮 SCANNING NEURAL DATABASE...'):
                results = []
                for attempt in range(3):
                    try:
                        api_response = requests.post(
                            "https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/recommend",
                            json={"genres": genres, "history": st.session_state.rec_history},
                            timeout=30
                        )
                        if api_response.status_code == 200:
                            results = [item["title"] for item in api_response.json().get("recommendations", [])]
                            st.session_state.rec_history.extend(results)
                            break
                        elif attempt < 2:
                            time.sleep(2)
                    except requests.exceptions.Timeout:
                        if attempt == 2:
                            st.warning("⏱️ AI is taking longer than usual. Try with fewer genres or try again later.")
                    except Exception as e:
                        if attempt == 2:
                            st.error("❌ Recommendation system temporarily unavailable. Please try again.")

                for r in results:
                    conn = sqlite3.connect("data/manhwa.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, image_url FROM manhwa WHERE title = ?", (r,))
                    result = cursor.fetchone()
                    conn.close()
                    if result:
                        manhwa_id, img = result
                        st.markdown(f"""
                        <div class="cyber-card" style="padding:10px; margin:10px 0;">
                            <a href="?id={manhwa_id}">
                                <img src="{img or 'https://via.placeholder.com/400x200'}" style="width:100%; height:150px; object-fit:cover; border-radius:8px;">
                            </a>
                            <p style="margin-top:8px; font-size:12px; text-align:center;">{r}</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    


# RUN
# ===============================
if __name__ == "__main__":
    main()