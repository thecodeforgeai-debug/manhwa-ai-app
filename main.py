import streamlit as st
import uuid
from datetime import datetime
import database
import ai_engine
from config import FREE_RECS_PER_DAY, PREMIUM_PRICE

st.set_page_config(
    page_title="Manhwa AI Recommender",
    page_icon="📚",
    layout="wide"
)

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'rec_count' not in st.session_state:
    st.session_state.rec_count = 0
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False

def main():
    with st.sidebar:
        st.title("📚 Manhwa AI")
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        Your AI-powered manhwa recommender!

        Get personalized recommendations based on genres, tropes, and mood.

        Analyze manhwa summaries to discover similar titles.
        """)

        st.markdown("---")
        st.markdown("### Your Usage")
        st.write(f"Recommendations today: {st.session_state.rec_count}/{FREE_RECS_PER_DAY}")

        if not st.session_state.is_premium:
            st.warning(f"Free tier: {FREE_RECS_PER_DAY} recs/day")
            if st.button("🌟 Upgrade to Premium", use_container_width=True):
                st.info(f"""
                **Premium Benefits:**
                - Unlimited recommendations
                - Priority support
                - Advanced features

                Only ${PREMIUM_PRICE}/month

                [Payment integration coming soon]
                """)
        else:
            st.success("✨ Premium Member")

        st.markdown("---")
        st.markdown("### Need Help?")
        st.markdown("""
        **Tips:**
        - Be specific with genres/tropes
        - Try different mood keywords
        - Use the trope analyzer for summaries
        """)

    st.title("🎨 Manhwa AI Recommender")
    st.markdown("*Discover your next favorite manhwa with AI-powered recommendations*")

    tab1, tab2 = st.tabs(["🔍 Get Recommendations", "🧠 Analyze Tropes"])

    with tab1:
        recommendation_tab()

    with tab2:
        analysis_tab()

def recommendation_tab():
    st.header("Find Your Next Read")

    col1, col2 = st.columns(2)

    with col1:
        genres = st.text_input(
            "Genres",
            placeholder="e.g., romance, isekai, fantasy",
            help="Enter genres separated by commas"
        )

        tropes = st.text_input(
            "Tropes",
            placeholder="e.g., enemies-to-lovers, reincarnation, strong-female-lead",
            help="Enter tropes separated by commas"
        )

    with col2:
        mood = st.text_input(
            "Mood/Vibe",
            placeholder="e.g., fluffy, dark, emotional, action-packed",
            help="Describe the mood you're looking for"
        )

        st.write("")
        st.write("")
        get_recs_button = st.button("✨ Get Recommendations", type="primary", use_container_width=True)

    if get_recs_button:
        if not st.session_state.is_premium and st.session_state.rec_count >= FREE_RECS_PER_DAY:
            st.error(f"You've reached your daily limit of {FREE_RECS_PER_DAY} recommendations. Upgrade to Premium for unlimited access!")
            return
        if not genres and not tropes and not mood:
        if not genres and not tropes and not mood:
            genre_list = [g.strip() for g in genres.split(",")] if genres else []
            trope_list = [t.strip() for t in tropes.split(",")] if tropes else []

        with st.spinner("🔮 Consulting the AI manhwa oracle..."):

            db_results = database.search_manhwa(
                limit=15
            )

            user_history = database.get_user_history(st.session_state.user_id, limit=3)

            result = ai_engine.get_recommendations(
                genres=genres,
                tropes=tropes,
                mood=mood,
                
                user_history=user_history if user_history else None
            )

            if result['success']:
                st.success("✅ Here are your personalized recommendations!")
                st.markdown(result['recommendations'])

                rec_titles = [m['title'] for m in db_results[:5]]
                database.save_user_history(
                    st.session_state.user_id,
                    genres,
                    tropes,
                    rec_titles
                )

                st.session_state.rec_count += 1
                
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")

    with st.expander("📊 Database Stats"):
        st.info(f"Currently tracking 10+ popular manhwa titles with more being added regularly!")

def analysis_tab():
    st.header("Analyze a Manhwa")

    st.markdown("""
    Paste a manhwa summary or description below, and AI will identify:
    - Key genres and tropes
    - Character archetypes
    - Similar manhwa recommendations
    """)

    summary = st.text_area(
        "Manhwa Summary",
        placeholder="Paste the manhwa description here...\n\nExample: 'A woman wakes up as the villainess in a novel she read. Knowing she's destined to die, she tries to avoid the main characters but ends up changing the story...'",
        height=200
    )

    analyze_button = st.button("🧠 Analyze", type="primary")

    if analyze_button:
        if not summary or len(summary.strip()) < 50:
            st.warning("Please provide a longer summary (at least 50 characters) for better analysis")
            return

        if not st.session_state.is_premium and st.session_state.rec_count >= FREE_RECS_PER_DAY:
            st.error(f"You've reached your daily limit of {FREE_RECS_PER_DAY} uses. Upgrade to Premium for unlimited access!")
            return

        with st.spinner("🔍 Analyzing tropes and patterns..."):
            result = ai_engine.analyze_tropes(summary)

            if result['success']:
                st.success("✅ Analysis Complete!")
                st.markdown(result['analysis'])

                st.session_state.rec_count += 1
                
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
