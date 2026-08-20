import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Analyzer", layout="wide")
st.title("📈 Indian Stock Market Analyzer")

# Sidebar
stock_list = {
   

pip install streamlit yfinance pandas plotly scikit-learn
streamlit run stock_analyzer.py