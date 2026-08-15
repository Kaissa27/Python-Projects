import streamlit as st
import pandas as pd
import sqlite3
import qrcode
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="WhatsApp Expense Splitter", layout="centered")
st.title("💸 WhatsApp Expense Splitter")
st.write("Split bills and send payment reminders on WhatsApp")

# DB Setup
conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()
c.execute