import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spotify Analytics", layout="wide")
st.title("🎧 Spotify Music Analytics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df['duration_min'] = df['duration_ms'] / 60000
    return df

df = load_data()

# --- FILTERS ---
st.sidebar.header("Filters")
genres = st.sidebar.multiselect("Select Genre", df['track_genre'].unique(), default=["pop", "hip-hop", "edm", "k-pop"])
filtered_df = df[df['track_genre'].isin(genres)]

# --- KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Tracks", f"{len(filtered_df):,}")
k2.metric("Avg Popularity", f"{filtered_df['popularity'].mean():.1f}/100")
k3.metric("Avg Danceability", f"{filtered_df['danceability'].mean():.2f}")
k4.metric("Avg Duration", f"{filtered_df['duration_min'].mean():.1f} min")

# --- CHARTS ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Top 10 Most Popular Tracks")
    top10 = filtered_df.sort_values('popularity', ascending=False).head(10)
    fig1 = px.bar(top10, x='popularity', y='track_name', orientation='h', color='track_genre')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Genre vs Popularity")
    genre_avg = filtered_df.groupby('track_genre')['popularity'].mean().reset_index().sort_values('popularity', ascending=False).head(10)
    fig2 = px.bar(genre_avg, x='track_genre', y='popularity', color='popularity', color_continuous_scale='Viridis')
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2) 
with c3:
    st.subheader("Danceability vs Energy (What makes a hit?)")
    fig3 = px.scatter(filtered_df.sample(5000), x='danceability', y='energy', color='popularity', size='loudness', hover_name='track_name')
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Audio Features Radar")
    features = ['danceability', 'energy', 'valence', 'acousticness', 'liveness']
    avg_features = filtered_df[features].mean().reset_index()
    avg_features.columns = ['feature', 'value']
    fig4 = px.line_polar(avg_features, r='value