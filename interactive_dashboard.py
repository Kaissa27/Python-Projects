import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

# Pinpoint the data warehouse file location
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "enterprise_warehouse.db"

# =====================================================================
# 1. WEB UI SETUP & SECURITY CHECK
# =====================================================================
st.set_page_config(page_title="Executive Revenue Dashboard", layout="wide")
st.title("📊 Executive Revenue Dashboard")
st.markdown("Interactive Business Intelligence Portal reading directly from our production database layer.")

if not DB_FILE.exists():
    st.error(f"❌ Database not found at `{DB_FILE}`. Please run the previous SQL script first to seed the data warehouse!")
else:
    # =====================================================================
    # 2. DATA EXTRACTION LAYER
    # =====================================================================
    with sqlite3.connect(DB_FILE) as conn:
        # Load the raw transaction data directly into an in-memory matrix
        df = pd.read_sql_query("SELECT * FROM server_transactions", conn)

    # =====================================================================
    # 3. INTERACTIVE SIDEBAR FILTERS
    # =====================================================================
    st.sidebar.header("Data Filter Control Panel")
    
    # Extract unique regional bounds dynamically from the dataset
    regions = list(df["region"].unique())
    selected_regions = st.sidebar.multiselect("Select Target Operating Regions:", regions, default=regions)
    
    # Slice the dataframe based on user filter selections
    filtered_df = df[df["region"].isin(selected_regions)]

    # =====================================================================
    # 4. EXECUTIVE LEVEL KPI CARDS
    # =====================================================================
    total_revenue = filtered_df["revenue"].sum()
    total_transactions = len(filtered_df)
    avg_transaction_value = filtered_df["revenue"].mean() if total_transactions > 0 else 0

    # Layout metrics horizontally in clean UI containers
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Gross Revenue", value=f"${total_revenue:,.2f}")
    kpi2.metric(label="Processed Transactions", value=f"{total_transactions:,} runs")
    kpi3.metric(label="Avg Ticket Size", value=f"${avg_transaction_value:,.2f}")

    st.markdown("---")

    # =====================================================================
    # 5. DYNAMIC DATA CHARTING & TABLES GRID
    # =====================================================================
    chart_column, table_column = st.columns([4, 3])

    with chart_column:
        st.subheader("📈 Revenue Capture by User Tier")
        if total_transactions > 0:
            # Aggregate metrics on the fly based on the user's active filter states
            tier_summary = filtered_df.groupby("user_tier")["revenue"].sum()
            
            # Matplotlib visual canvas rendering
            fig, ax = plt.subplots(figsize=(6, 3.5))
            tier_summary.plot(kind="bar", color=["#3498db", "#2ecc71", "#e74c3c"], ax=ax)
            ax.set_ylabel("Accumulated Revenue ($)")
            ax.set_xlabel("Account Subscription Classification")
            ax.grid(axis='y', linestyle='--', alpha=0.4)
            plt.xticks(rotation=0)
            
            # Stream the matplotlib canvas directly into the web layout container
            st.pyplot(fig)
        else:
            st.warning("No data rows comply with your current sidebar filter constraints.")

    with table_column:
        st.subheader("📋 Filtered Audit Ledger")
        # Display the data frame as an interactive spreadsheet component
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
