import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="YouTube Analytics", layout="wide")
st.title("📺 YouTube Channel Analytics Dashboard")

@st.cache_data
def load_data():
    # Replace with your csv - "Global YouTube Statistics.csv" or your API export
    df = pd.read_csv("Global YouTube Statistics.csv", encoding='latin1')
    # Clean columns
    df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')
    df['video views'] = pd.to_numeric(df['video views'], errors='coerce')
    df['uploads'] = pd.to_numeric(df['uploads'], errors='coerce')
    df['Engagement Rate'] = (df['subscribers'] / df['video views'] * 100).fillna(0)
    return df

df = load_data()

# --- FILTERS ---
st.sidebar.header("Filters")
category = st.sidebar.multiselect("Select Category", df['category'].dropna().unique(), default=df['category'].dropna().unique()[:3])
filtered_df = df[df['category'].isin(category)]

# --- KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Channels", f"{len(filtered_df):,}")
k2.metric("Total Subscribers", f"{filtered_df['subscribers'].sum()/1e9:.2f}B")
k3.metric("Total Views", f"{filtered_df['video views'].sum()/1e12:.2f}T")
k4.metric("Avg Views / Video", f"{(filtered_df['video views']/filtered_df['uploads']).mean():,.0f}")

# --- CHARTS ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Top 10 Channels by Subscribers")
    top10 = filtered_df.sort_values('subscribers', ascending=False).head(10)
    fig1 = px.bar(top10, x='subscribers', y='Youtuber', orientation='h', color='category')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Category vs Average Views")
    cat_avg = filtered_df.groupby('category')['video views'].mean().reset_index().sort_values('video views', ascending=False)
    fig2 = px.pie(cat_avg, names='category', values='video views', hole=0.5)
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.subheader("Subscribers vs Views")
    fig