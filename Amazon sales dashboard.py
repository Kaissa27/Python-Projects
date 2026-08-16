import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Amazon Sales Dashboard")
st.write("Upload your sales data CSV")

uploaded = st.file_uploader("Upload CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{df['Sales'].sum():,.0f}")
    col2.metric("Total Orders", f"{df['Orders'].sum():,.0f}")
    col3.metric("Avg Order Value", f"₹{df['Sales'].sum()/df['Orders'].sum():.0f}")
    
    # Top Products
    st.subheader("Top 10 Products by Sales")
    top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(top_products, orientation='h')
    st.plotly_chart(fig, use_container_width=True)
    
    # Sales by Category
    st.subheader("Sales by Category")
    cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.pie(cat_sales, names='Category', values='Sales')
    st.plotly_chart(fig2)
    
    # Monthly Trend
    df['Date'] = pd.to_datetime(df['Date'])
    monthly = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly['Date'] = monthly['Date'].astype(str)
    fig3 = px.line(monthly, x='Date', y='Sales', title='Monthly Revenue Trend')
    st.plotly_chart(fig3)
    
    st.download_button("Download Analysis", df.to_csv().encode(), "analysis.csv")