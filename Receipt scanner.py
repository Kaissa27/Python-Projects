pip install streamlit pandas qrcode[pil] pillow pytesseract

import streamlit as st
import pandas as pd
import sqlite3
import qrcode
from io import BytesIO
import urllib.parse
import re
from PIL import Image
import pytesseract

st.set_page_config(page_title="Smart Expense Splitter", layout="centered")
st.title("💸 Smart Expense Splitter + Receipt Scanner")
st.write("Upload bill → Auto read amount → Split with friends")

# DB Setup
conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, trip TEXT, person TEXT, amount REAL, description TEXT)''')
conn.commit()

trip_name = st.sidebar.text_input("Trip/Group Name", "Goa Trip")
members_input = st.sidebar.text_area("Members", "Riya, Aman, Priya, You")
members = [m.strip() for m in members_input.split(",")]

# OCR FUNCTION
def scan_receipt(image):
    text = pytesseract.image_to_string(image)

    # Extract amount - looks for ₹ or Rs or Total
    amount_match = re.findall(r'(?:total|amount|rs|₹)\D*([\d,]+\.?\d{0,2})', text.lower())
    amount = float(amount_match[-1].replace(',', '')) if amount_match else 0.0

    # Extract shop name - usually first 2 lines
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    shop_name = lines[0] if lines else "Receipt"

    return amount, shop_name, text

# 1. RECEIPT UPLOAD
st.subheader("1. Scan Receipt")
uploaded_file = st.file_uploader("Upload Receipt Image", type=['jpg','jpeg','png'])

scanned_amount = 0.0
scanned_desc = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", width=300)

    with st.spinner("Reading receipt..."):
        scanned_amount, scanned_desc, full_text = scan_receipt(image)

    st.success(f"Detected: {scanned_desc} - ₹{scanned_amount}")
    with st.expander("See full extracted text"):
        st.text(full_text)

# 2. ADD EXPENSE
st.subheader("2. Add Expense")
col1, col2, col3 = st.columns(3)
with col1:
    paid_by = st.selectbox("Paid by", members)
with col2:
    amount = st.number_input("Amount ₹", value=scanned_amount, min_value=0.0, step=100.0)
with col3:
    description = st.text_input("For what?", value=scanned_desc)

if st.button("Add Expense"):
    c.execute("INSERT INTO expenses (trip, person, amount, description) VALUES (?,?,?,?)",
              (trip_name, paid_by, amount, description))
    conn.commit()
    st.success(f"Added: {paid_by} paid ₹{amount} for {description}")

# 3. SHOW SPLIT
st.subheader("3. Split Summary")
df = pd.read_sql_query(f"SELECT * FROM expenses WHERE trip='{trip_name}'", conn)
if not df.empty:
    st.dataframe(df[['person', 'amount', 'description']], use_container_width=True)

    total = df['amount'].sum()
    split = total / len(members)
    st.metric("Total Spent", f"₹{total}")
    st.metric("Per Person Share", f"₹{split:.2f}")

    balances = {m: df[df['person']==m]['amount'].sum() - split for m in members}
    owes = {k: v for k, v in balances.items() if v < 0}
    gets = {k: v for k, v in balances.items() if v > 0}

    transactions = []
    for debtor, debt_amt in owes.items():
        for creditor, credit_amt in gets.items():
            if debt_amt < 0 and credit_amt > 0:
                pay = min(-debt_amt, credit_amt)
                transactions.append(f"{debtor} → {creditor}: ₹{pay:.2f}")
                owes[debtor] += pay
                gets[creditor] -= pay

    for t in transactions:
        st.write("👉", t)

    # WhatsApp Message
    phone = st.text_input("Receiver WhatsApp number", "91XXXXXXXXXX")
    msg = f"*{trip_name} Expense Split*\n\nTotal: ₹{total:.2f} | Per Head: ₹{split:.2f}\n\n" + "\n".join(transactions)
    whatsapp_url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
    st.markdown(f"[Send on WhatsApp]({whatsapp_url})")

else:
    st.info("Upload a receipt or add expenses manually")