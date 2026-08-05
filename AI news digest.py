import streamlit as st
from GoogleNews import GoogleNews
import newspaper
from gtts import gTTS
import os

st.title("📰 AI News Podcast Generator")

category = st.selectbox("Category", ["Technology", "India", "Business", "Sports"])

def get_news(category):
    googlenews = GoogleNews(lang='en', region='IN')
    googlenews.search(category)
    results = googlenews.results()[:5] # top 5
    
    summaries = []
    for article in results:
        try:
            news = newspaper.Article(article['link'])
            news.download()
            news.parse()
            summary = news.text[:500] # first 500 chars
            summaries.append(f"{article['title']}: {summary}")
        except:
            continue
    return summaries

def text_to_speech(text):
    tts = gTTS(text, lang='en')
    tts.save("news.mp3")
    return "news.mp3"

if st.button("Generate Today's News"):
    news_list = get_news(category)
    full_text = " ".join(news_list)
    
    st.subheader("Summary")
    for n in news_list:
        st.write(f"- {n[:200]}...")
    
    audio_file = text_to_speech(full_text[:2000])
    st.audio(audio_file)
    st.download_button("Download Podcast", audio_file)