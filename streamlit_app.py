import streamlit as st
import random
import time

# Page config
st.set_page_config(
    page_title="MANHWA AI RECOMMENDER",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CYBER SEOUL CSS
st.markdown("""
<style>
    /* CYBER SEOUL BASE */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%) !important;
        font-family: 'Rajdhani', 'Segoe UI', sans-serif !important;
        color: #e0e0ff !important;
    }
    
    /* GLITCH HEADER */
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }
    
    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }
    
    @keyframes neonPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
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
        margin-bottom: 10px !important;
        letter-spacing: 1px !important;
    }
    
    h2 {
        color: #00ffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.5) !important;
        border-left: 4px solid #ff00ff !important;
        padding-left: 15px !important;
        margin-top: 30px !important;
        animation: neonPulse 3s infinite !important;
    }
    
    h3 {
        color: #ff00ff !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        margin-top: 20px !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }
    
    /* SCANLINE EFFECT */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            transparent 50%,
            rgba(0, 255, 255, 0.03) 50%
        );
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 9999;
        animation: scanline 8s linear infinite;
    }
    
    /* GRID OVERLAY */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 9998;
    }
    
    /* CYBER CARDS */
    .cyber-card {
        background: rgba(10, 10, 26, 0.8) !important;
        border: 2px solid !important;
        border-image: linear-gradient(45deg, #00ffff, #ff00ff) 1 !important;
        border-radius: 10px !important;
        padding: 25px !important;
        margin: 20px 0 !important;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.3),
            inset 0 0 20px rgba(0, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .cyber-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #00ffff);
        z-index: -1;
        filter: blur(10px);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .cyber-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 
            0 0 30px rgba(0, 255, 255, 0.5),
            inset 0 0 30px rgba(0, 255, 255, 0.2) !important;
    }
    
    .cyber-card:hover::before {
        opacity: 0.5;
    }
    
    /* RANK BADGES */
    .rank-badge {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 40px !important;
        height: 40px !important;
        background: linear-gradient(45deg, #ff00ff, #00ffff) !important;
        color: #0a0a1a !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border-radius: 50% !important;
        margin-right: 15px !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.7) !important;
    }
    
    /* CYBER BUTTONS */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #ff00ff) !important;
        color: #0a0a1a !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        width: 100% !important;
        margin: 10px 0 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        z-index: 1 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s ease;
        z-index: -1;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 10px 25px rgba(0, 255, 255, 0.4),
            0 10px 25px rgba(255, 0, 255, 0.4) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* SPLIT SCREEN COLUMNS */
    [data-testid="column"] {
        background: rgba(16, 16, 32, 0.6) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        margin: 10px !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        box-shadow: 
            inset 0 0 20px rgba(0, 255, 255, 0.1),
            0 0 30px rgba(0, 255, 255, 0.1) !important;
    }
    
    /* METRIC DISPLAY */
    .cyber-metric {
        font-size: 42px !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #00ffff, #ff00ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
        margin: 10px 0 !important;
    }
    
    .cyber-metric-label {
        color: #a0a0ff !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    /* GLITCH TEXT */
    .glitch-text {
        position: relative;
        display: inline-block;
    }
    
    .glitch-text::before,
    .glitch-text::after {
        content: attr(data-text);
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    
    .glitch-text::before {
        color: #ff00ff;
        animation: glitch 0.3s infinite;
        clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%);
    }
    
    .glitch-text::after {
        color: #00ffff;
        animation: glitch 0.3s infinite reverse;
        clip-path: polygon(0 55%, 100% 55%, 100% 100%, 0 100%);
    }
    
    /* HIDE STREAMLIT DEFAULTS */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Cyber Seoul Main App
def main():
    # HEADER with glitch effect
    st.markdown("<h1 class='glitch-text' data-text='MANHWA AI RECOMMENDER'>MANHWA AI RECOMMENDER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a0a0ff;'>Discover your next favorite manhwa with neural-powered recommendations</h3>", unsafe_allow_html=True)
    
    # Split-screen columns (60/40 split)
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        # TRENDING TODAY - Gangnam District
        st.markdown("<h2>𓊝 TRENDING DISTRICT</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #a0a0ff; font-size: 16px;'>Neural scan of Gangnam's most discussed titles</p>", unsafe_allow_html=True)
        
        # Card 1 - Solo Leveling
        with st.container():
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; align-items: center;'>", unsafe_allow_html=True)
            st.markdown("<div class='rank-badge'>1</div><h3 style='margin: 0;'>SOLO LEVELING</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<div class='cyber-metric'>892</div>", unsafe_allow_html=True)
                st.markdown("<div class='cyber-metric-label'>TODAY'S SCORE</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='cyber-metric'>2,847</div>", unsafe_allow_html=True)
                st.markdown("<div class='cyber-metric-label'>TOTAL SCAN</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div style='background: linear-gradient(45deg, #00ff00, #00ffff); padding: 10px 15px; border-radius: 20px; text-align: center;'>", unsafe_allow_html=True)
                st.markdown("<div style='color: #0a0a1a; font-weight: 900; font-size: 18px;'>+127</div>", unsafe_allow_html=True)
                st.markdown("<div style='color: #0a0a1a; font-size: 12px;'>TODAY</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='color: #00ffff; margin-top: 15px; font-size: 16px; letter-spacing: 1px;'>ACTION · FANTASY · GAME ELEMENTS</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Card 2 - The Beginning After The End
        with st.container():
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; align-items: center;'>", unsafe_allow_html=True)
            st.markdown("<div class='rank-badge'>2</div><h3 style='margin: 0;'>THE BEGINNING AFTER THE END</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='color: #ff00ff; margin: 10px 0;'>FANTASY · REINCARNATION</div>", unsafe_allow_html=True)
            st.markdown("<div class='cyber-metric'>745</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Card 3 - Omniscient Reader
        with st.container():
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; align-items: center;'>", unsafe_allow_html=True)
            st.markdown("<div class='rank-badge'>3</div><h3 style='margin: 0;'>OMNISCIENT READER</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='color: #ff00ff; margin: 10px 0;'>FANTASY · APOCALYPSE</div>", unsafe_allow_html=True)
            st.markdown("<div class='cyber-metric'>698</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
        if st.button("𓊝 INITIATE RECOMMENDATION SCAN", key="scan_btn"):
            st.session_state.scan_initiated = True
        
        if st.button("𓊝 ANALYZE NEURAL PATTERNS", key="analyze_btn"):
            st.session_state.analyze = True
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        # NEURAL INTERFACE
        st.markdown("<h2>𓊝 NEURAL INTERFACE</h2>", unsafe_allow_html=True)
        
        # Genres Selector
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ffff; margin-top: 0;'>GENRES</h3>", unsafe_allow_html=True)
        genres = st.multiselect(
            "Select neural preferences",
            ["ACTION", "FANTASY", "CYBERPUNK", "ROMANCE", "THRILLER", "MYSTERY", "SCIFI", "SUPERNATURAL"],
            default=["ACTION", "FANTASY"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mood Selector
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ffff; margin-top: 0;'>MOOD/VIBE</h3>", unsafe_allow_html=True)
        mood = st.selectbox(
            "Select neural frequency",
            ["ACTION-PACKED AND INTENSE", "CYBERNOIR MYSTERY", "NEON ROMANCE", "EPIC FANTASY", "PSYCHOLOGICAL THRILLER"],
            index=0,
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Tropes Selector
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ffff; margin-top: 0;'>TROPES (OPTIONAL)</h3>", unsafe_allow_html=True)
        tropes = st.multiselect(
            "Select narrative patterns",
            ["SYSTEM", "REINCARNATION", "CYBER-ENHANCEMENT", "TIME TRAVEL", "DUNGEON CRAWL", "APOCALYPSE"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Scan Button
        if st.button("𓊝 INITIATE DEEP SCAN", key="deep_scan"):
            st.session_state.deep_scan = True
        
        # Results Display
        if st.session_state.get('scan_initiated', False) or st.session_state.get('deep_scan', False):
            st.markdown("<div class='cyber-card' style='border-image: linear-gradient(45deg, #00ff00, #00ffff) 1;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #00ff00;'>𓊝 NEURAL SCAN RESULTS</h3>", unsafe_allow_html=True)
            
            results = [
                {"title": "SOLO LEVELING", "match": "98%", "status": "𓊝 OPTIMAL MATCH"},
                {"title": "OMNISCIENT READER", "match": "92%", "status": "𓊝 HIGH SYNC"},
                {"title": "TOWER OF GOD", "match": "87%", "status": "𓊝 NEURAL COMPATIBLE"}
            ]
            
            for result in results:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{result['title']}**")
                    st.markdown(f"<div style='color: #a0a0ff; font-size: 14px;'>{result['status']}</div>", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"<div style='background: linear-gradient(45deg, #00ff00, #00ffff); color: #0a0a1a; padding: 5px 10px; border-radius: 15px; text-align: center; font-weight: 900;'>{result['match']}</div>", unsafe_allow_html=True)
                st.markdown("---")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # System Status
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00ffff; margin-top: 0;'>𓊝 SYSTEM STATUS</h3>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-metric'>2/3</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #a0a0ff;'>NEURAL QUERIES TODAY</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #8888ff; font-size: 14px; margin-top: 10px;'>FREE TIER: 3 RESULTS PER CYCLE</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Upgrade Banner
    st.markdown("""
    <div style='
        background: linear-gradient(45deg, #ff00ff, #00ffff);
        color: #0a0a1a;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 30px 0;
        font-weight: 900;
        font-size: 24px;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
        animation: neonPulse 2s infinite;
    '>
    𓊝 UPGRADE TO NEURAL PREMIUM 𓊝
    </div>
    """, unsafe_allow_html=True)
    
    # Terminal Footer
    st.markdown("<div style='color: #00ff00; font-family: monospace; font-size: 12px; text-align: center; border-top: 1px solid #00ffff; padding-top: 10px;'>", unsafe_allow_html=True)
    st.markdown("𓊝 SYSTEM: ONLINE | NEURAL NET: ACTIVE | GANGSEC: STABLE 𓊝", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Initialize session state
for key in ['scan_initiated', 'analyze', 'deep_scan']:
    if key not in st.session_state:
        st.session_state[key] = False

if __name__ == "__main__":
    main()
                           # Cyber Seoul App
