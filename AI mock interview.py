import streamlit as st
import google.generativeai as genai

st.title("🎤 AI Mock Interviewer")

role = st.selectbox("Select Role", ["Python Developer", "Data Analyst", "SDE"])

# Configure Gemini
genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.score = 0

def ask_question(role, history):
    prompt = f"You are an interviewer for {role}. Ask 1 question. Previous Q&A: {history}. Be professional."
    response = model.generate_content(prompt)
    return response.text

def give_feedback(answer):
    prompt = f"Rate this interview answer out of 10 and give 2 improvement tips: {answer}"
    response = model.generate_content(prompt)
    return response.text

if st.button("Start Interview"):
    q = ask_question(role, st.session_state.questions)
    st.session_state.questions.append({"q": q})
    st.write(f"**Interviewer:** {q}")

user_answer = st.text_area("Your Answer")
if st.button("Submit Answer"):
    feedback = give_feedback(user_answer)
    st.info(feedback)
    st.session_state.questions[-1]["a"] = user_answer