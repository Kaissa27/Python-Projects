import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="YouTube Analytics", layout="wide")
st.title("📊 YouTube Channel Analytics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("youtube_data.csv") # Your exported data
    df['publish_time'] = pd.to_datetime(df['publish_time'])
    df['day'] = df['publish_time'].dt.day_name()
    df['hour'] = df['publish_time'].dt.hour