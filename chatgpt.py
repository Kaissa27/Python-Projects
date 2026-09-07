import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My ChatGPT Clone", page_icon="🤖", layout="wide")
st.title("Project 28: Build ChatGPT Clone - AI Chatbot")

# --- SETUP ---
st.sidebar.title(" Settings")
st.sidebar.write("Get FREE API Key from: platform.openai.com")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password", help="sk-....")

model = st.sidebar.selectbox("Choose Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
role = st.sidebar.selectbox("Chatbot Role",
    ["Data Science Mentor", "Resume Reviewer", "SQL Expert", "Python Tutor", "Business Analyst", "Custom"])

if role == "Custom":
    custom_prompt = st.sidebar.text_area("Custom System Prompt", "You are a helpful assistant.")
else:
    prompts = {
        "Data Science Mentor": "You are a senior Data Scientist with 10 years experience at Google. You teach beginners in simple language with code examples.",
        "Resume Reviewer": "You are an expert resume reviewer for Data Analyst roles. Give specific, actionable feedback. Be strict but helpful.",
        "SQL Expert": "You are a SQL expert. Whenever user asks a question, give SQL query + explanation + optimized version.",
        "Python Tutor": "You are a Python tutor. Always give code with comments, explain logic simply, and give practice exercise.",
        "Business Analyst": "You are a Business Analyst. Convert any business problem into KPI, analysis plan, and dashboard idea."
    }
    custom_prompt = prompts[role]

st.sidebar.divider()
st.sidebar.info(" Cost: gpt-4o-mini = FREE-ish ( $0.15 per 1M tokens). 1 conversation = < 1 paisa")

# --- CHAT UI ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": custom_prompt}]

# Display chat history (skip system)
for msg in st.session_state.messages:
    if msg["role"]!= "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input
if prompt := st.chat_input(f"Ask {role}..."):
    if not api_key:
        st.warning("Please enter OpenAI API Key in sidebar to make it work. It's free!")
        st.info("For demo without API, here is how it would work:")
        st.code(f"""
User: {prompt}
Bot ({role}): [This is where AI response would come with API key]

System Prompt used: {custom_prompt}
Model: {model}
        """)
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            client = OpenAI(api_key=api_key)
            stream = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                stream=True
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

# --- BUSINESS IDEA SECTION ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("How to Make Money")
    st.write("""
    1. **Resume Reviewer Bot** - Sell to students for Rs 299
    2. **SQL Practice Bot** - For data analyst aspirants
    3. **Company Chatbot** - Charge businesses Rs 10k to build for their website
    """)

with col2:
    st.subheader("Deploy & Sell")
    st.code("""
    1. Deploy on Streamlit Cloud - FREE
    2. Add Razorpay payment link
    3. Share on LinkedIn: "I built ChatGPT for Resumes"
    4. You will get 5-10 paid users in first week
    """)

with col3:
    st.subheader(" Resume Point - MOST POWERFUL")
    st.code("""
Built ChatGPT Clone using OpenAI API (GPT-4o-mini)
with 5 custom roles: Mentor, Resume Reviewer,
SQL Expert, Python Tutor, Business Analyst

Features: Streaming response, custom system
prompts, chat history, low cost ($0.15/1M tokens)

Tech: Python, OpenAI API, Streamlit, Prompt Engineering
    """, language="text")

# --- NO API KEY VERSION (FREE) ---
with st.expander("Don't have API Key? Use FREE version with Groq/Hugging Face"):
    st.code("""
# FREE ALTERNATIVE - No OpenAI needed, use Groq (free)

from groq import Groq

client = Groq(api_key="gsk_...") # FREE from groq.com

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant", # FREE & FAST
    messages=[{"role":"user","content":"Explain SQL Joins"}],
)

print(completion.choices[0].message.content)

# Groq gives FREE API - 14,400 requests per day FREE
# Faster than OpenAI
    """, language="python")
    st.link_button("Get FREE Groq API Key", "https://console.groq.com/keys")

st.success(" Project DONE - YOU CAN NOW BUILD & SELL AI CHATBOTS")
st.balloons()