import streamlit as st
import pypdf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("📄 AI Resume ATS Checker")

resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

def extract_text(pdf):
    reader = pypdf.PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ats_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(similarity * 100, 2)

if st.button("Check Score") and resume_file and job_desc:
    resume_text = extract_text(resume_file)

    score = ats_score(resume_text, job_desc)

    st.metric("ATS Match Score", f"{score}%")

    if score >= 75:
        st.success("Great! ATS friendly resume")
    elif score >= 50:
        st.warning("Medium. Add more keywords from JD")
    else:
        st.error("Low match. Tailor resume to job description")

    # Show missing keywords
    jd_words = set(job_desc.lower().split())
    resume_words = set(resume_text.lower().split())
    missing = jd_words - resume_words
    st.write("**Missing Keywords:**", ", ".join(list(missing)[:15])) 