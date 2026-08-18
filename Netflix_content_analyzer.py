import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Analysis", layout="wide")
st.title("🎬 Netflix Content Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv") # Kaggle dataset
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Titles", len(df))
col2.metric("Movies", len(df[df['type']=='Movie']))
col3.metric("TV Shows", len(df[df['type']=='TV Show']))
col4.metric("Countries", df['country'].nunique())

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Content Added Over Years")
    yearly = df.groupby('year_added')['show_id'].count().reset_index()
    fig1 = px.line(yearly, x='year_added', y='show_id', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col