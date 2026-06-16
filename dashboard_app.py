import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

# Locate our production data warehouse
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "production_analytics.db"

# =====================================================================
# 1. UI HEADER CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Data Pipeline Command Center", layout="wide")
st.title("⚙️ Data Pipeline Command Center")
st.markdown("Real-time telemetry and extraction analytics from background automation daemons.")

# Verify database infrastructure exists before loading
if not DB_FILE.exists():
    st.error(f"🔴 Data Warehouse file not detected at `{DB_FILE}`. Run your extraction pipeline first to log metrics!")
else:
    # =====================================================================
    # 2. DATA EXTRACTION LAYER
    # =====================================================================
    with sqlite3.connect(DB_FILE) as conn:
        # Load the entire log table into memory for interactive slicing
        df = pd.read_sql_query("SELECT * FROM web_audit_logs ORDER BY timestamp DESC", conn)

    # =====================================================================
    # 3. INTERACTIVE SIDEBAR FILTERS
    # =====================================================================
    st.sidebar.header("Filter Engine")
    status_options = list(df["status"].unique())
    selected_statuses = st.sidebar.multiselect("Execution Outcome Status:", status_options, default=status_options)
    
    # Filter dataset dynamically based on user selections
    filtered_df = df[df["status"].isin(selected_statuses)]

    # =====================================================================
    # 4. EXECUTIVE METRIC KPI CARDS
    # =====================================================================
    total_runs = len(filtered_df)
    success_rate = (len(filtered_df[filtered_df["status"] == "Success"]) / total_runs * 100) if total_runs > 0 else 0
    avg_chars = filtered_df["char_count"].mean() if total_runs > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Tasks Audited", value=f"{total_runs:,} runs")
    col2.metric(label="Pipeline Success Rate", value=f"{success_rate:.1f}%")
    col3.metric(label="Avg Character Payload", value=f"{avg_chars:.1f} bytes")

    st.markdown("---")

    # =====================================================================
    # 5. SPLIT-SCREEN ANALYTICS GRID
    # =====================================================================
    left_chart_col, right_data_col = st.columns([1, 1])

    with left_chart_col:
        st.subheader("📊 Outcome Distribution Matrix")
        if total_runs > 0:
            status_counts = filtered_df["status"].value_counts()
            
            # Matplotlib plotting configuration
            fig, ax = plt.subplots(figsize=(5, 3.5))
            colors = ['#2ecc71' if state == 'Success' else '#e74c3c' for state in status_counts.index]
            ax.bar(status_counts.index, status_counts.values, color=colors, width=0.5)
            ax.set_ylabel("Total Cycles")
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            
            st.pyplot(fig)
        else:
            st.info("No records match your filter constraints.")

    with right_data_col:
        st.subheader("📋 Transaction Log Ledger")
        # Display the live data frame as an interactive spreadsheet component
        st.dataframe(
            filtered_df[["id", "search_term", "char_count", "status", "timestamp"]],
            use_container_width=True,
            hide_index=True
        )
