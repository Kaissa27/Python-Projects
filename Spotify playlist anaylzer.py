import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import plotly.express as px

# Get these from Spotify Developer Dashboard
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501"

scope = "user-library-read playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI, scope=scope))

st.title("🎵 Spotify Playlist Analyzer")

if st.button("Connect Spotify"):
    results = sp.current_user_top_artists(limit=10)
    
    artists = [item['name'] for item in results['items']]
    popularity = [item['popularity'] for item in results['items']]
    
    fig = px.bar(x=artists, y=popularity, title="Your Top 10 Artists")
    st.plotly_chart(fig)
    
    st.write("**Top Genres:**")
    genres = [g for artist in results['items'] for g in artist['genres']]
    st.write(pd.Series(genres).value_counts().head(10))