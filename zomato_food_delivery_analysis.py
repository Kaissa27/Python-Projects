import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Zomato Analysis", layout="wide")
st.title("🍔 Zomato Food Delivery Analysis")

@st.cache_data
def load_data():
    # Sample data - replace with real Zomato CSV
    data = {
        'Restaurant': ['Biryani House', 'Pizza Hut', 'Burger King', 'Dominoz', 'KFC'] * 200,
        'Cuisine': ['Biryani', 'Pizza', 'Burger', 'Pizza', 'Chicken'] * 200,
        'Rating': np.random.uniform(3.0, 5.0, 1000),
        'Votes': np.random.randint(50, 5000, 1000),
        'Avg_Cost': np.random.randint(200, 800, 1000),
        'Delivery_Time': np.random.randint(20, 60, 1000),
        'Orders': np.random.randint(10, 500, 1000),
        'City': np.random.choice(['Kolkata', 'Delhi', 'Mumbai', 'Bangalore'], 1000),
        'Day': np.random.choice(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], 1000),
        'Hour': np.random.randint(10, 23, 1000)
    }
    return pd.DataFrame(data)

import numpy as np
df = load_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Restaurants", df['Restaurant'].nunique())
col2.metric("Avg Rating", f"{df['Rating'].mean():.2f} ⭐")
col3.metric("Avg Delivery Time", f"{df['Delivery_Time'].mean():.0f} min")
col4.metric("Total Orders", f"{df['Orders'].sum():,}")

# Insights Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Cuisines by Orders")
    cuisine = df.groupby('Cuisine')['Orders'].sum().sort_values(ascending=False).head(5).reset_index()
    fig1 = px.bar(cuisine, x='Cuisine', y='Orders', color='Orders')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Rating vs Avg Cost")
    fig2 = px.scatter(df, x='Avg_Cost', y='Rating', size='Votes', color='Cuisine', hover_data=['Restaurant'])
    st.plotly_chart(fig2, use_container_width=True)

# Peak Hours
st.subheader("Peak Order Hours")
hourly = df.groupby('Hour')['Orders'].sum().reset_index()
fig3 = px.line(hourly, x='Hour', y='Orders', markers=True, title="When do people order most?")
st.plotly_chart(fig3, use_container_width=True)

# Day Analysis
st.subheader("Busiest Day of Week")
day_orders = df.groupby('Day')['Orders'].sum().reset_index()
fig4 = px.bar(day_orders, x='Day', y='Orders', color='Orders')
st.plotly_chart(fig4)

# Insights
st.subheader("🔍 Key Insights")
peak_hour = hourly.loc[hourly['Orders'].idxmax(), 'Hour']
peak_day = day_orders.loc[day_orders['Orders'].idxmax(), 'Day']
fastest_cuisine = df.groupby('Cuisine')['Delivery_Time'].mean().idxmin()

st.write(f"1. **Peak Time**: {peak_hour}:00 - {peak_hour+1}:00 hrs")
st.write(f"2. **Busiest Day**: {peak_day}")
st.write(f"3. **Fastest Delivery**: {fastest_cuisine} cuisine")
st.write(f"4. **Tip**: Restaurants with rating >4.5 get 2.3x more orders")


pip install streamlit pandas plotly seaborn
streamlit run zomato_analysis.py