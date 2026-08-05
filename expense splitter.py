import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from io import BytesIO

st.title("💸 Group Expense Splitter")

DB = "expenses.db"
conn = sqlite3.connect(DB)
conn.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, group_name TEXT, item TEXT,
              amount REAL, paid_by TEXT, members TEXT, date TEXT)''')

group = st.selectbox("Group", ["Goa Trip", "Hostel", "Friends"])
item = st.text_input("What was it?")
amount = st.number_input("Amount ₹", 0.0)
paid_by = st.text_input("Paid by")
members = st.text_input("Split between: comma separated").split(",")

if st.button("Add Expense"):
    conn.execute("INSERT INTO expenses VALUES (NULL,?,?,?,?,?,date('now'))",
                 (group, item, amount, paid_by, ",".join(members)))
    conn.commit()
    st.success("Added!")

df = pd.read_sql("SELECT * FROM expenses WHERE group_name=?", conn, params=(group,))

if not df.empty:
    st.dataframe(df)

    # Calculate balances
    balances = {}
    for _, row in df.iterrows():
        split = row['amount'] / len(row['members'].split(","))
        for m in row['members'].split(","):
            balances[m] = balances.get(m, 0) - split
        balances[row['paid_by']] = balances.get(row['paid_by'], 0) + row['amount']

    st.subheader("Who owes what:")
    for person, bal in balances.items():
        if bal > 0:
            st.write(f"{person} should receive ₹{bal:.2f}")
        elif bal < 0:
            st.write(f"{person} should pay ₹{abs(bal):.2f}")