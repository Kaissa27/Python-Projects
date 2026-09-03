import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Your Name - Data Analyst Portfolio", layout="wide", page_icon="🚀")

# --- HEADER ---
st.title("🚀 Hi, I'm [Your Name] - Data Analyst")
st.subheader("Python | SQL | Power BI | Streamlit | 24+ Projects")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Projects", "25+")
c2.metric("Technologies", "10+")
c3.metric("Dashboards", "15+")
c4.link_button("Download Resume", "https://your-resume-link.com")

st.divider()

# --- TABS FOR ALL PROJECTS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Sales & Finance", "👥 Marketing & Customer", "🚚 Operations", "📱 Social Media", "🤖 AI Chatbot"])

with tab1:
    st.subheader("Sales Dashboard - Superstore")
    st.write("Tech: Python, Plotly, Streamlit | Sales up 22% after analysis")
    # Add your screenshot / iframe
    st.image("https://via.placeholder.com/800x400?text=Sales+Dashboard+Screenshot")
    st.link_button("Live Demo - Project 1", "#")

    st.subheader("Financial KPI Dashboard")
    st.image("https://via.placeholder.com/800x400?text=Finance+Dashboard")

with tab2:
    st.subheader("RFM Customer Segmentation + K-Means")
    st.write("Clustered 800 customers into VIP / Loyal / At Risk - 65% revenue from VIP")
    st.image("https://via.placeholder.com/800x400?text=RFM+Dashboard")

with tab3:
    st.subheader("Supply Chain - Late Delivery Risk")
    st.write("Analyzed 180k orders, 55% late - Saved $1.2M at risk")
    st.image("https://via.placeholder.com/800x400?text=Supply+Chain+Dashboard")

with tab4:
    st.subheader("YouTube & Instagram Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.write("YouTube - 1M Views Analysis")
        st.image("https://via.placeholder.com/400x300?text=YouTube+Analytics")
    with col2:
        st.write("Instagram - 1.2M Reach Analysis")
        st.image("https://via.placeholder.com/400x300?text=Instagram+Analytics")

with tab5:
    st.subheader("🤖 Ask AI About My Resume")
    st.write("Recruiter can ask: What are your skills? Show your best project?")
    
    # Simple Chatbot without API key - using rule based
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask about my resume... e.g. What is your experience with SQL?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # --- FAKE AI LOGIC (Replace with OpenAI API later) ---
        answer = ""
        p = prompt.lower()
        if "sql" in p:
            answer = "I have done 5 SQL projects including Sales Analysis where I wrote 50+ queries with Window Functions, CTEs, Joins to find top customers and YoY growth."
        elif "python" in p:
            answer = "I have 25 projects in Python using Pandas, Plotly, Scikit-learn. Built RFM Segmentation, Churn Prediction, and Supply Chain Risk model."
        elif "power bi" in p:
            answer = "I have created 8 Power BI dashboards including Sales, HR Attrition, and Finance dashboards with DAX and Row Level Security."
        elif "project" in p:
            answer = "My best project is RFM + K-Means Segmentation (Project 21) and Supply Chain Risk Dashboard (Project 22). Both are deployed on Streamlit and show business impact of $1.2M."
        else:
            answer = "I am a Data Analyst with 25+ projects in Python, SQL, Power BI, Streamlit. I specialize in Sales, Marketing, and Operations Analytics. Check my tabs for live demos!"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)

st.divider()
st.subheader("📬 Contact Me")
st.write("Email: yourname@gmail.com | LinkedIn: linkedin.com/in/yourname | GitHub: github.com/yourname")

with st.expander("📌 How to deploy this for FREE"):
    st.code("""
    1. Push all 25 projects to GitHub
    2. Go to share.streamlit.io -> Deploy this app.py
    3. Buy domain for Rs 500/year from GoDaddy -> yourname.com
    4. Link Streamlit app to domain
    5. Add this link to your Resume TOP - Recruiter will click and get WOWed
    
    This portfolio alone = Interview Call
    """)

st.balloons()
st.success("🎉 CONGRATULATIONS - YOU COMPLETED 25 PROJECTS - YOU ARE NOW JOB READY DATA ANALYST")