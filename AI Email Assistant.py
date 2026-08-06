import streamlit as st
import google.generativeai as genai

st.title("📧 AI Email Assistant")

# Dummy emails for demo - replace with Gmail API
emails = [
    {"from": "hr@company.com", "subject": "Interview Scheduled", "body": "Hi, your interview is on 10th Aug 3pm"},
    {"from": "newsletter@tech.com", "subject": "Weekly Tech Digest", "body": "Latest AI news..."},
    {"from": "bank@hdfc.com", "subject": "Bill Payment Due", "body": "Your credit card bill 5420 due on 12th Aug"}
]

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize_email(email):
    prompt = f"Summarize this email in 1 line and mark priority High/Med/Low: {email['subject']} {email['body']}"
    return model.generate_content(prompt).text

def draft_reply(email, tone):
    prompt = f"Write a {tone} reply to this email: {email['body']}"
    return model.generate_content(prompt).text

for email in emails:
    with st.expander(f"{email['subject']} - from {email['from']}"):
        summary = summarize_email(email)
        st.write("**AI Summary:**", summary)
        
        tone = st.selectbox("Reply tone", ["Professional", "Friendly", "Short"], key=email['subject'])
        if st.button("Generate Reply", key=email['subject']+"btn"):
            reply = draft_reply(email, tone)
            st.code(reply)