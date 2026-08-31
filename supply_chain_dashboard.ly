import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("Supply Chain - Late Delivery Risk Dashboard")

@st.cache_data
def load_data():
    # Try DataCo dataset, fallback to Superstore logic
    try:
        df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding='latin1')
        df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
        df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])
    except:
        # Fallback for Superstore users
        df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
        df['Delivery_Days'] = (df['Ship Date'] - df['Order Date']).dt.days
        df['Late_Delivery_Risk'] = df['Delivery_Days'].apply(lambda x: 1 if x > 5 else 0)
        df['Department Name'] = df['Category']
        df['Shipping Mode'] = df['Ship Mode']
        df['Sales'] = df['Sales']
        return df
    return df

df = load_data()

# Create Risk if not present
if 'Late_Delivery_Risk' not in df.columns:
    df['Late_Delivery_Risk'] = df['Delivery Status'].apply(lambda x: 1 if x=='Late delivery' else 0)

# --- KP