import streamlit as st
from summarizer import summarize_article
from classifier import classify_topic
from utils import fetch_articles, generate_newsletter

st.set_page_config(page_title="AI News Curator", layout="wide")
st.title("🗞️ Personal AI News Curator")
st.markdown("Select your topics of interest and get a daily summary of the top news!")

# --- Sidebar for topic selection ---
available_topics = [
    "technology", "science", "business", "sports", "health", "entertainment", "politics", "world"
]

selected_topics = st.sidebar.multiselect(
    "Choose your preferred topics:", available_topics, default=["technology", "science"]
)

# --- Main logic ---
if st.button("🔍 Curate My News"):
    st.info("Fetching and summarizing articles...")

    articles = fetch_articles()
    if not articles:
        st.warning("No articles found.")
    else:
        summarized_articles = []
        for article in articles:
            summary = summarize_article(article["text"])
            topic = classify_topic(summary)

            if topic.lower() in selected_topics:
                summarized_articles.append({
                    "title": article["title"],
                    "summary": summary,
                    "topic": topic
                })

        if summarized_articles:
            st.success(f"Found {len(summarized_articles)} relevant articles.")
            for art in summarized_articles:
                st.subheader(art["title"])
                st.write(f"**Topic:** {art['topic']}")
                st.write(art["summary"])
                st.markdown("---")

            generate_newsletter(summarized_articles)
            st.markdown("📧 [Download Newsletter](newsletter.html)", unsafe_allow_html=True)
        else:
            st.warning("No articles matched your selected topics.")
