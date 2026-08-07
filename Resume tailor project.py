import streamlit as st
import pdfplumber
import google.generativeai as genai

st.title("🎯 AI Resume Tailor")

resume_file = st.file_uploader("Upload Master Resume PDF", type="pdf")
jd_text = st.text_area("Paste Job Description")

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text(pdf):
    text = ""
    with pdfplumber.open(pdf) as pdf_obj:
        for page in pdf_obj.pages:
            text += page.extract_text()
    return text

def tailor_resume(resume, jd):
    prompt = f"""You are a career coach. Tailor this resume to match the JD.
    Rules: Keep truth, only rephrase. Add JD keywords. Use action verbs. ATS optimized.
    
    RESUME: {resume}
    JD: {jd}
    
    Output: 1. Tailored Resume 2. 3 bullet points changed + why"""
    return model.generate_content(prompt).text

if st.button("Tailor My Resume"):
    resume_text = extract_text(resume_file)
    tailored = tailor_resume(resume_text, jd_text)
    st.subheader("Tailored Resume")
    st.write(tailored)
    st.download_button("Download as TXT", tailored)