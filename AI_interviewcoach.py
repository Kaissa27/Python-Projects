import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import speech_recognition as sr

st.title("🎤 AI Interview Coach")
st.write("Upload Resume + JD. Get mock interviews with instant feedback")

# Sidebar inputs
resume_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_desc = st.text_area("Paste Job Description:", placeholder="Software Engineer at Google...")

# Load LLM - free HuggingFace model
@st.cache_resource
def load_llm():
    return HuggingFaceHub(
        repo_id="google/flan-t5-large",
        huggingfacehub_api_token=""