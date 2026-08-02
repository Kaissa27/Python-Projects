import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
import sqlite3

API_KEY = "YOUR_API_KEY" # Get from Google Cloud Console
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_stats(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    data = response['items'][0]
    return {
        'title