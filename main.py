# CYBER NOIR - Eye-friendly cyber theme
st.markdown("""
<style>
    /* CYBER NOIR BASE - Softer on eyes */
    .stApp {
        background: linear-gradient(135deg, #121212 0%, #1a1a1a 30%, #202020 100%) !important;
        font-family: 'Segoe UI', 'Roboto', sans-serif !important;
        color: #e0e0e0 !important;
    }
    
    /* Subtle grid overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.5;
    }
    
    /* HEADER - Cool but calm */
    h1 {
        font-size: 44px !important;
        font-weight: 800 !important;
        text-align: center !important;
        background: linear-gradient(90deg, #7B68EE, #00BFFF, #7B68EE) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: shimmer 4s ease-in-out infinite !important;
        margin-bottom: 10px !important;
        letter-spacing: -0.5px !important;
    }
    
    @keyframes shimmer {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
    
    /* Subheader */
    [data-testid="stMarkdownContainer"] h3 {
        text-align: center !important;
        color: #a0a0a0 !important;
        font-weight: 400 !important;
        font-size: 18px !important;
        margin-bottom: 40px !important;
    }
    
    /* Section headers */
    h2 {
        color: #7B68EE !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin-top: 35px !important;
        margin-bottom: 8px !important;
        border-left: 4px solid #00BFFF !important;
        padding-left: 12px !important;
    }
    
    /* Section subheaders */
    [data-testid="stMarkdownContainer"] h2 + p {
        color: #888 !important;
        font-size: 14px !important;
        margin-top: 0 !important;
        margin-bottom: 25px !important;
        font-weight: 300 !important;
    }
    
    /* CARDS - Soft glow */
    .cyber-card {
        background: rgba(25, 25, 35, 0.8) !important;
        border: 1px solid rgba(123, 104, 238, 0.3) !important;
        border-radius: 12px !important;
        padding: 22px !important;
        margin: 18px 0 !important;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .cyber-card:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(123, 104, 238, 0.6) !important;
        box-shadow: 
            0 8px 30px rgba(123, 104, 238, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Rank badges */
    .rank-badge {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 36px !important;
        height: 36px !important;
        background: linear-gradient(135deg, #7B68EE, #00BFFF) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border-radius: 50% !important;
        margin-right: 12px !important;
        box-shadow: 0 4px 12px rgba(123, 104, 238, 0.4) !important;
    }
    
    /* BUTTONS - Elegant glow */
    .stButton > button {
        background: linear-gradient(135deg, #7B68EE, #00BFFF) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(123, 104, 238, 0.4) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Metrics - Clean display */
    .cyber-metric {
        font-size: 38px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #7B68EE, #00BFFF) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 12px 0 !important;
    }
    
    .cyber-metric-label {
        color: #a0a0a0 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 500 !important;
    }
    
    /* Columns */
    [data-testid="column"] {
        background: rgba(30, 30, 40, 0.6) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    /* Form elements */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(40, 40, 50, 0.8) !important;
        border: 1px solid rgba(123, 104, 238, 0.3) !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: rgba(123, 104, 238, 0.6) !important;
        box-shadow: 0 0 15px rgba(123, 104, 238, 0.2) !important;
    }
    
    /* Upgrade banner */
    [data-testid="stAlert"] {
        background: linear-gradient(90deg, rgba(123, 104, 238, 0.15), rgba(0, 191, 255, 0.15)) !important;
        border: 1px solid rgba(123, 104, 238, 0.3) !important;
        border-radius: 10px !important;
        color: #d0d0ff !important;
        font-weight: 600 !important;
    }
    
    /* Hide defaults */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)
                           