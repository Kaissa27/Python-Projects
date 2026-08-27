import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Airbnb Analytics", layout="wide")
st.title("Airbnb Price Predictor & Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv("AB_NYC_2019.csv")
    df = df.dropna(subset=['price','room_type','neighbourhood_group'])
    return df

df = load_data()

# --- SIDEBAR PREDICTOR ---
st.sidebar.header("Predict Your Listing Price")
room = st.sidebar.selectbox("Room Type", df['room_type'].unique())
neigh = st.sidebar.selectbox("Area", df['neighbourhood_group'].unique())
min_nights = st.sidebar.slider("Minimum Nights", 1, 30, 3)
reviews = st.sidebar.slider("Number of Reviews", 0, 500, 20)
availability = st.sidebar.slider("Availability Days", 0, 365, 100)

# --- KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Listings", f"{len(df):,}")
k2.metric("Avg Price", f"${df['price'].mean():.0f}")
k3.metric("Avg Reviews", f"{df['number_of_reviews'].mean():.0f}")
k4.metric("Most Listings", df['neighbourhood_group'].mode()[0])

c1, c2 = st.columns(2)
with c1:
    st.subheader("Price by Room Type")
    fig1 = px.box(df, x='room_type', y='price', color='room_type')
    fig1.update_layout(yaxis_range=[0,500])
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Top Areas by Average Price")
    area_price = df.groupby('neighbourhood_group')['price'].mean().reset_index()
    fig2 = px.bar(area_price, x='neighbourhood_group', y='price', color='price')
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.subheader("Price vs Reviews")
    fig3 = px.scatter(df.sample(5000), x='number_of_reviews', y='price', color='room_type', log_y=True)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Listings on Map")
    st.map(df.sample(1000)[['latitude','longitude']].dropna())

# --- ML MODEL ---
st.subheader(" ML Price Predictor (Random Forest)")
df_model = df[['room_type','neighbourhood_group','minimum_nights','number_of_reviews','availability_365','price']].copy()
df_model = pd.get_dummies(df_model, columns=['room_type','neighbourhood_group'])

X = df_model.drop('price', axis=1)
y = df_model['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
acc = model.score(X_test, y_test