import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Kolkata AirBnB", layout="wide")
st.title("🏠 Kolkata AirBnB Price Predictor")

@st.cache_data
def load_data():
    df = pd.read_csv("kolkata_airbnb.csv") # Kaggle dataset
    df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
    return df

df = load_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Listings", len(df))
col2.metric("Avg Price/Night", f"₹{df['price'].mean():.0f}")
col3.metric("Most Expensive Area", df.groupby('neighbourhood')['price'].mean().idxmax())
col4.metric("Avg Reviews", f"{df['reviews'].mean():.1f}")

# Map
st.subheader("📍 Listings Map")
fig_map = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                            color="price", size="reviews",
                            hover_name="neighbourhood",
                            mapbox_style="carto-positron", zoom=10)
st.plotly_chart(fig_map)

# Price by Location
col1, col2 = st.columns(2)
with col1:
    st.subheader("Avg Price by Area")
    area_price = df.groupby('neighbourhood')['price'].mean().sort_values().reset_index()
    fig1 = px.bar(area_price, x='price', y='neighbourhood', orientation='h')
    st.plotly_chart(fig1)

with col2:
    st.subheader("Price vs Reviews")
    fig2 = px.scatter(df, x='reviews', y='price', color='room_type')
    st.plotly_chart(fig2)

# ===== ML MODEL =====
st.subheader("🤖 Predict Your Listing Price")

# Preprocess
le_hood = LabelEncoder()
le_room = LabelEncoder()
df['hood_enc'] = le_hood.fit_transform(df['neighbourhood'])
df['room_enc'] = le_room.fit_transform(df['room_type'])

features = ['hood_enc', 'room_enc', 'bedrooms', 'bathrooms', 'reviews', 'minimum_nights']
X = df[features]
y = df['price']

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# User Input
col1, col2, col3 = st.columns(3)
with col1:
    neighbourhood = st.selectbox("Area", df['neighbourhood'].unique())
with col2:
    room_type = st.selectbox("Room Type", df['room_type'].unique())
with col3:
    bedrooms = st.slider("Bedrooms", 1, 5, 2)

bathrooms = st.slider("Bathrooms", 1, 3, 1)
reviews = st.slider("Expected Reviews", 0, 200, 20)
nights = st.slider("Minimum Nights", 1, 30, 2)

if st.button("Predict Price"):
    hood_num = le_hood.transform([neighbourhood])[0]
    room_num = le_room.transform([room_type])[0]
    input_data = [[hood_num, room_num, bedrooms,