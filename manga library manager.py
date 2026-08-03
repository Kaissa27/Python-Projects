import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="My Library", layout="wide")
DB = "library.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, 
                  type TEXT, status TEXT, rating REAL, pages INTEGER, 
                  pages_read INTEGER, genre TEXT, notes TEXT)''')
    conn.commit()
    conn.close()

def add_book(title, author, type, status, pages, genre):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO books VALUES (NULL,?,?,?,?,?,?,?,?)",
                 (title, author, type, status, 0, pages, 0, genre, ""))
    conn.commit()
    conn.close()

init_db()
st.title("📚 My Manga & Book Library")

with st.sidebar:
    st.header("Add Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    type = st.selectbox("Type", ["Manga","Book","Novel","Webtoon"])
    status = st.selectbox("Status", ["To Read","Reading","Completed","On Hold"])
    pages = st.number_input("Total Pages", 1, 5000)
    genre = st.text_input("Genre")
    if st.button("Add"):
        add_book(title, author, type, status, pages, genre)

conn = sqlite3.connect(DB)
df = pd.read_sql("SELECT * FROM books", conn)
conn.close()

if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Books", len(df))
    col2.metric("Completed", len(df[df.status=="Completed"]))
    col3.metric("Reading", len(df[df.status=="Reading"]))
    
    fig = px.pie(df, names='genre', title='Books by Genre')
    st.plotly_chart(fig)
    
    st.dataframe(df)
else:
    st.info("Add your first book to start!")