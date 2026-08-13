import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

# For free local LLM, we use HuggingFace models
# No OpenAI key needed

st.title("📖 AI Study Buddy")
st.write("Upload your PDF and ask anything about it")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    # Step 1: Read PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    st.success(f"Loaded {len(pdf_reader.pages)} pages")

    # Step 2: Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size