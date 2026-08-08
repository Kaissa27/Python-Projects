import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

st.title("💰 AI Finance Advisor")

uploaded_file = st.file_uploader("Upload Bank CSV", type="csv")

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def categorize_expense(desc):
    categories = {
        'zomato|swiggy': 'Food',
        'uber|ola|metro': 'Travel', 
        'amazon|flipkart': 'Shopping',
        'rent|electricity': 'Bills'
    }
    for key, cat in categories.items():
        if any(k in desc.lower() for k in key.split('|')):
            return cat
    return 'Other'

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Category'] = df['Description'].apply(categorize_expense)
    
    fig = px.pie(df, values='Amount', names='Category', title='Monthly Spending')
    st.plotly_chart(fig)
    
    question = st.text_input("Ask about your spending")
    if question:
        context = df.groupby('Category')['Amount'].sum().to_string()
        prompt = f"Based on this spending data: {context}. Answer: {question}"
        answer = model.generate_content(prompt).text
        st.info(answer)