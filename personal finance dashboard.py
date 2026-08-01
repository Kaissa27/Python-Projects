import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Finance Dashboard", layout="wide")
DB = "finance.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, date TEXT, type TEXT, 
                  category TEXT, amount REAL, note TEXT)''')
    conn.commit()
    conn.close()

def add_transaction(date, t_type, category, amount, note):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO transactions VALUES (NULL,?,?,?,?,?)",
                 (date, t_type, category, amount, note))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df

init_db()
st.title("💰 Personal Finance Dashboard")

# Sidebar form
with st.sidebar:
    st.header("Add Transaction")
    date = st.date_input("Date")
    t_type = st.selectbox("Type", ["income", "expense"])
    category = st.text_input("Category")
    amount = st.number_input("Amount ₹", min_value=0.0)
    note = st.text_input("Note")
    if st.button("Add"):
        add_transaction(date, t_type, category, amount, note)
        st.success("Added!")

# Main dashboard
df = load_data()
if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{df[df.type=='income'].amount.sum()}")
    col2.metric("Total Expense", f"₹{df[df.type=='expense'].amount.sum()}")
    col3.metric("Balance", f"₹{df[df.type=='income'].amount.sum() - df[df.type=='expense'].amount.sum()}")
    
    # Charts
    expense_df = df[df.type=='expense']
    fig = px.pie(expense_df, names='category', values='amount', title='Spending by Category')
    st.plotly_chart(fig, use_container_width=True)
    
    monthly = df.groupby([df.date.dt.to_period('M'), 'type']).amount.sum().reset_index()
    fig2 = px.bar(monthly, x='date', y='amount', color='type', title='Monthly Income vs Expense')
    st.dataframe(df)
else:
    st.info("Add your first transaction to see charts")