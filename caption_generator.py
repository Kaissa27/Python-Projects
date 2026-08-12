import streamlit as st
import random
from datetime import datetime

# Caption templates
CAPTION_TEMPLATES = {
    "food": [
        "Kolkata cravings hit different 🤤 {topic}",
        "POV: You found the best {topic} in Kolkata",
        "Adding this to my food diary 📖 {topic}",
        "Cheap, tasty, Kolkata approved ✨ {topic}",
        "Tag someone who needs to try this {topic} with you!"
    ],
    "travel": [
        "Collecting moments, not things ✈️ {topic}",
        "Lost in {topic} and loving it",
        "Wanderlust level: 100 {topic}",
        "New city, new memories {topic}",
        "This is my happy place: {topic}"
    ],
    "lifestyle": [
        "Just me and my {topic} era 💫",
        "Romanticizing the little things: {topic}",
        "Soft life, good vibes {topic}",
        "That {topic} feeling",
        "Manifesting more of this {topic}"
    ]
}

HASHTAG_BANK = {
    "food": ["#foodie", "#kolkatafood", "#streetfood", "#foodporn", "#indianfood", "#yummy", "#foodblogger", "#eatlocal", "#foodlover", "#kolkatadiaries"],
    "travel": ["#travel", "#wanderlust", "#explore", "#adventure", "#travelgram", "#vacation", "#trip", "#nature", "#photography", "#travelindia"],
    "lifestyle": ["#lifestyle", "#aesthetic", "#vibes", "#daily", "#mood", "#selfcare", "#life", "#goodvibes", "#inspiration", "#motivation"],
    "general": ["#trending", "#reels", "#viral", "#instagood", "#love", "#photooftheday", "#fyp", "#explorepage"]
}

POSTING_TIMES = {
    "Instagram": ["11 AM - 1 PM", "6 PM - 9 PM"],
    "Threads": ["9 AM - 11 AM", "7 PM - 10 PM"]
}

def generate_captions(topic, niche):
    templates = CAPTION_TEMPLATES.get(niche, CAPTION_TEMPLATES["lifestyle"])
    captions = [t.format(topic=topic) for t in random.sample(templates, 5)]
    return captions

def generate_hashtags(topic, niche):
    niche_tags = HASHTAG_BANK.get(niche, [])
    general_tags = HASHTAG_BANK["general"]
    hashtags = random.sample(niche_tags, 10) + random.sample(general_tags, 10)
    return ["#" + topic.replace(" ", "")] + hashtags

st.title("📱 Caption + Hashtag Generator")
st.write("For Instagram & Threads")

topic = st.text_input("Enter your post topic:", placeholder="e.g. food vlog Kolkata, sunset beach")
niche = st.selectbox("Pick niche:", ["food", "travel", "lifestyle", "general"])

if st.button("Generate 🚀"):
    if topic:
        st.subheader("✨ 5 Caption Ideas")
        captions = generate_captions(topic, niche)
        for i, cap in enumerate(captions, 1):
            st.text_area(f"Caption {i}", cap, height=70)
        
        st.subheader("🏷️ 20 Hashtags")
        hashtags = generate_hashtags(topic, niche)
        st.code(" ".join(hashtags))
        
        st.subheader("⏰ Best Time to Post")
        for platform, times in POSTING_TIMES.items():
            st.write(f"**{platform}**: {', '.join(times)}")
    else:
        st.warning("Please enter a topic first!")

st.caption("Tip: Mix 10 niche + 10 general hashtags for best reach")