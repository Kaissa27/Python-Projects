import streamlit as st
import pypdf
import sqlite3

st.title("AI Study Buddy")

uploaded_file = st.file_uploader("Upload Notes PDF", type=["pdf"])

def extract_text(pdf):
    reader = pypdf.PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text[:3000] # limit for API

def generate_questions(text):
    # This would call Gemini/OpenAI API
    prompt = f"Generate 5 MCQ questions from this text:\n{text}"
    # response = client.models.generate_content(prompt)
    return ["Q1: What is...?", "Q2: Explain..."] # placeholder

if uploaded_file:
    text = extract_text(uploaded_file)
    st.success("Notes loaded!")
    
    if st.button("Generate Quiz"):
        questions = generate_questions(text)
        for i, q in enumerate(questions):
            st.write(f"**{q}**")
            answer = st.text_input(f"Your Answer {i+1}")