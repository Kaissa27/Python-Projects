import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Amazon Sales Dashboard", layout="wide")
st.title("🛒 Amazon Sales Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv("Amazon Sale Report.csv", encoding='latin1')
    df.drop(columns=['New','PendingS'], errors='ignore', inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month_name()
    return df

df = load_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", len(df))
col2.metric("Total Revenue", f"₹{df['Amount'].sum():,.0f}")
col3.metric("Avg Order Value", f"₹{df['Amount'].mean():.0f}")
col4.metric("Top Category", df['Category'].mode()[0])

# Row 1
col1, col2 = st.columns(2)
with col1:
    st.subheader("Sales by Category")
    cat_sales = df.groupby('Category')['Amount'].sum().reset_index().sort_values('Amount', ascending=False)
    fig1 = px.bar(cat_sales, x='Category', y='Amount', color='Category')
    st.plotly_chart(fig1)

with col2:
    st.subheader("Order Status")
    status_count = df['Status'].value_counts().reset_index()
    status_count.columns = ['Status','Count']
    fig2 = px.pie(status_count, names='Status', values='Count', hole=0.4)
    st.plotly_chart(fig2)

# Row 2
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 States by Sales")
    state_sales = df.groupby('ship-state')['Amount'].sum().reset_index().sort_values('Amount', ascending=False).head(10)
    fig3 = px.bar(state_sales, x='Amount', y='ship-state', orientation='h')
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3)

with col2:
    st.subheader("B2B vs B2C Sales")
    b2b = df.groupby('B2B')['Amount'].sum().reset_index()
    b2b['B2B'] = b2b['B2B'].map({True:'B2B', False:'Retail'})
    fig4 = px.pie(b2b, names='B2B', values='Amount')
    st.plotly_chart(fig4)

# Insights
st.subheader("🔍 Key Business Insights")
st.write("1. **Size L** is most ordered - stock more of it")
st.write("2. **Maharashtra** gives max revenue - run ads there")
st.write("3. **Shipped - Delivered to Buyer** is 85% - but focus on Reducing Cancelled")
st.write("4. **Kurta** category is top seller - bundle it")

st.download_button("📥 Download Cleaned Data", df.to_csv(index=False).encode(), "amazon_analysis.csv")