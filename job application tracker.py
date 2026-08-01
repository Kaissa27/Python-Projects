import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Job Tracker", layout="wide")
DB = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY, company TEXT, role TEXT, 
                  status TEXT, link TEXT, salary TEXT, 
                  date_applied TEXT, follow_up_date TEXT, notes TEXT)''')
    conn.commit()
    conn.close()

def add_job(company, role, status, link, salary, date_applied, follow_up, notes):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO applications VALUES (NULL,?,?,?,?,?,?,?,?)",
                 (company, role, status, link, salary, date_applied, follow_up, notes))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM applications", conn)
    conn.close()
    return df

init_db()
st.title("💼 Job Application Tracker")

# Sidebar form
with st.sidebar:
    st.header("Add Application")
    company = st.text_input("Company")
    role = st.text_input("Role")
    status = st.selectbox("Status", ["Wishlist","Applied","Interview","Offer","Rejected"])
    link = st.text_input("Job Link")
    salary = st.text_input("Salary Range")
    date_applied = st.date_input("Date Applied")
    follow_up = st.date_input("Follow Up Date")
    notes = st.text_area("Notes")
    if st.button("Add"):
        add_job(company, role, status, link, salary, date_applied, follow_up, notes)
        st.success("Added!")

df = load_data()
if not df.empty:
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Apps", len(df))
    col2.metric("Interviews", len(df[df.status=="Interview"]))
    col3.metric("Offers", len(df[df.status=="Offer"]))
    col4.metric("Response Rate", f"{len(df[df.status!='Wishlist'])/len(df)*100:.1f}%")
    
    # Status Pipeline Chart
    fig = px.bar(df['status'].value_counts(), title="Applications by Status")
    st.plotly_chart(fig)
    
    # Upcoming follow ups
    today = datetime.now().date()
    due = df[pd.to_datetime(df.follow_up_date).dt.date <= today + timedelta(days=3)]
    if not due.empty:
        st.warning("⚠️ Follow ups due soon")
        st.dataframe(due[['company','role','follow_up_date']])
    
    st.dataframe(df)
else:
    st.info("Add your first job application")