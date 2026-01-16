import streamlit as st
import urllib.parse
import requests

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
def google_search(title: str):
    return f"https://www.google.com/search?q={urllib.parse.quote(title + ' manhwa')}"

# ===============================
# MAIN APP
# ===============================
def main():

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
        st.markdown("</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1])

    # ===============================
    # LEFT — TRENDING
    # ===============================
    with col_left:
        st.markdown("<h2>𓊝 TRENDING DISTRICT</h2>", unsafe_allow_html=True)

        # Fetch trending from API
        try:
            response = requests.get("https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/trending", timeout=5)
            data = response.json()
            trending = [(item["title"], item["image"]) for item in data]
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            trending = [("API Error", "https://via.placeholder.com/400x560")]

        # Create 2 rows of 5 manhwa each
        row1 = st.columns(5, gap="small")
        row2 = st.columns(5, gap="small")
        
        for i, (title, img) in enumerate(trending[:10]):
            link = google_search(title)
            col = row1[i] if i < 5 else row2[i - 5]
            
            with col:
                st.markdown(f"""
                <div class="cyber-card" style="padding:10px; height:350px;">
                    <div class="rank-badge" style="position:absolute; top:10px; left:10px; width:28px; height:28px; font-size:14px;">{i+1}</div>
                    <a href="{link}" target="_blank">
                        <img src="{img}" style="width:100%; height:250px; object-fit:cover;">
                    </a>
                    <p style="margin-top:8px; font-size:11px; line-height:1.3; overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">{title}</p>
                </div>
                """, unsafe_allow_html=True)

    # ===============================
    # RIGHT — NEURAL INTERFACE
    # ===============================
    with col_right:
        st.markdown("<h2>𓊝 NEURAL INTERFACE</h2>", unsafe_allow_html=True)

        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
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
            st.markdown("<h3>𓊝 NEURAL RESULTS</h3>", unsafe_allow_html=True)

            # Show loading animation
            with st.spinner('🔮 SCANNING NEURAL DATABASE...'):
                try:
                    api_response = requests.post(
                        "https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/recommend",
                        json={"genres": genres, "history": st.session_state.rec_history},
                        timeout=30
                    )
                    results = [item["title"] for item in api_response.json().get("recommendations", [])]
                    st.session_state.rec_history.extend(results)  # Track recommendations
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
                    results = ["AI Error - Please try again"]

            for r in results:
                link = google_search(r)
                st.markdown(f"""
                <a href="{link}" target="_blank" style="text-decoration:none;">
                    <div style="padding:10px 0; color:#00ffff; font-weight:700;">
                        {r}
                    </div>
                </a>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    

            st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    main()