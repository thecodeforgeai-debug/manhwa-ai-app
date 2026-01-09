import streamlit as st
import ai_engine
import database

st.set_page_config(
    page_title="Manhwa AI Recommender",
    page_icon="📚",
    layout="wide"
)

GENRES = [
    "action", "romance", "fantasy", "drama", "comedy", "horror", "thriller",
    "psychological", "isekai", "martial-arts", "sci-fi", "supernatural",
    "adventure", "mystery", "school", "office", "historical", "apocalypse",
    "game", "slice-of-life", "sports", "military"
]

TROPES = [
    "overpowered-mc", "weak-to-strong", "strong-female-lead", "time-travel",
    "reincarnation", "regression", "revenge", "underdog-to-hero",
    "enemies-to-lovers", "fake-dating", "contract-relationship", "boss-employee",
    "love-triangle", "arranged-marriage", "age-gap", "game-elements",
    "tower-climbing", "dungeon", "leveling", "survival", "smart-mc",
    "found-family", "mentor-student", "magic", "cultivation", "mercenary",
    "body-swap", "villain-protagonist", "anti-hero", "redemption",
    "second-chance", "political-intrigue", "supernatural-powers", "monsters",
    "bullying", "transformation", "curse"
]

MOODS = [
    "Action-packed and intense", "Light and funny", "Dark and serious",
    "Romantic and sweet", "Emotional and touching", "Mysterious and suspenseful",
    "Epic and grand", "Relaxing and wholesome", "Thrilling and scary",
    "Inspiring and motivational"
]

st.title("🎨 Manhwa AI Recommender")
st.markdown("*Discover your next favorite manhwa with AI-powered recommendations*")

with st.sidebar:
    st.header("📚 Manhwa AI")
    st.markdown("---")
    st.subheader("About")
    st.markdown("Your AI-powered manhwa recommender! Get personalized recommendations based on genres, tropes, and mood.")
    st.markdown("---")
    st.subheader("Your Usage")
    if 'recs_count' not in st.session_state:
        st.session_state.recs_count = 0
    st.metric("Recommendations today:", f"{st.session_state.recs_count}/3")
    st.caption("Free tier: 3 recs/day")
    st.button("⭐ Upgrade to Premium")
    st.markdown("---")
    st.subheader("Need Help?")
    st.markdown("**Tips:**\n- Select multiple genres\n- Try different tropes\n- Mix and match!")

tab1, tab2 = st.tabs(["🔍 Get Recommendations", "🧠 Analyze Tropes"])

with tab1:
    st.header("Find Your Next Read")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Genres")
        selected_genres = st.multiselect(
            "Select one or more genres",
            options=GENRES,
            default=["action"],
            help="Choose the genres you're interested in"
        )
    
    with col2:
        st.subheader("Mood/Vibe")
        selected_mood = st.selectbox(
            "What vibe are you looking for?",
            options=MOODS,
            help="Select the mood that matches what you want"
        )
    
    st.subheader("Tropes")
    selected_tropes = st.multiselect(
        "Select your favorite tropes (optional)",
        options=TROPES,
        help="Choose story elements you enjoy"
    )
    
    if st.button("✨ Get Recommendations", type="primary", use_container_width=True):
        if not selected_genres and not selected_tropes and not selected_mood:
            st.warning("Please select at least one preference (genre, trope, or mood)")
        elif st.session_state.recs_count >= 3:
            st.error("You've reached your daily limit of 3 recommendations. Upgrade to Premium for unlimited access!")
        else:
            with st.spinner("🔮 Consulting the AI manhwa oracle..."):
                user_history = database.get_user_history(st.session_state.get('user_id', 'default'), limit=3)
                result = ai_engine.get_recommendations(
                    genres=selected_genres if selected_genres else [],
                    tropes=selected_tropes if selected_tropes else [],
                    mood=selected_mood,
                    user_history=user_history if user_history else None
                )
                
                if result['success']:
                    st.success("✅ Here are your personalized recommendations!")
                    st.markdown(result['recommendations'])
                    st.session_state.recs_count += 1
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
    
    with st.expander("📊 Database Stats"):
        stats = database.get_stats()
        if stats:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Manhwa", stats.get('total', 0))
            with col2:
                st.metric("Genres", len(set(GENRES)))
            with col3:
                st.metric("Tropes", len(set(TROPES)))

with tab2:
    st.header("Analyze Manhwa Tropes")
    st.markdown("Enter a manhwa summary to discover what tropes it contains!")
    
    manhwa_summary = st.text_area(
        "Paste manhwa summary here:",
        height=150,
        placeholder="Enter a plot summary...",
        help="Paste a summary from anywhere"
    )
    
    if st.button("🔍 Analyze Tropes", type="primary", use_container_width=True):
        if not manhwa_summary:
            st.warning("Please enter a manhwa summary to analyze")
        else:
            with st.spinner("🧠 Analyzing tropes..."):
                result = ai_engine.analyze_tropes(manhwa_summary)
                if result['success']:
                    st.success("✅ Analysis complete!")
                    st.markdown(result['analysis'])
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")

st.markdown("---")
st.caption("Made with ❤️ using Claude AI")
