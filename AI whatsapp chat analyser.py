import streamlit as st
import pandas as pd
import re
import google.generativeai as genai
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("📱 AI WhatsApp Analyzer")

chat_file = st.file_uploader("Upload WhatsApp.txt export", type="txt")

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_chat(file):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}) - (.*?): (.*)'
    data = []
    for line in file.read().decode('utf-8').split('\n'):
        match = re.match(pattern, line)
        if match:
            data.append(match.groups())
    return pd.DataFrame(data, columns=['Date', 'Time', 'Sender', 'Message'])

if chat_file:
    df = parse_chat(chat_file)
    st.metric("Total Messages", len(df))
    st.metric("Most Active", df['Sender'].value_counts().index[0])

    # Wordcloud
    text = " ".join(df['Message'])
    wc = WordCloud().generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    st.pyplot(fig) 

    if st.button("AI Summary"):
        sample = "\n".join(df['Message'].tail(100))
        prompt = f"Summarize this WhatsApp chat. Topics, mood, who talks most, 1 funny insight: {sample}"
        summary = model.generate_content(prompt).text
        st.info(summary)