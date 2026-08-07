import streamlit as st
import google.generativeai as genai

st.title("💼 LinkedIn Post Generator")

idea = st.text_area("What's your idea?")
style = st.selectbox("Post Style", ["Story", "Listicle", "Hot Take", "Lesson"])

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_post(idea, style):
    prompt = f"""Write a LinkedIn post in {style} style about: {idea}
    Rules: Hook in first line, 3-5 short paragraphs, end with CTA + 5 hashtags.
    Target: Tech professionals in India"""
    response = model.generate_content(prompt)
    return response.text

if st.button("Generate 3 Posts"):
    for i in range(3):
        post = generate_post(idea, style)
        st.subheader(f"Option {i+1}")
        st.write(post)
        st.download_button("Copy Post", post, key=i)