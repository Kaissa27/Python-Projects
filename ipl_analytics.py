import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="IPL Analytics", layout="wide")
st.title(" IPL Analytics Dashboard 2008-2024")

# Load Data
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# Clean data
matches['date'] = pd.to_datetime(matches['date'])

# Sidebar
st.sidebar.header("Filters")
seasons = st.sidebar.multiselect("Select Season", sorted(matches['season'].unique()), default=[2023,2024])
teams = st.sidebar.multiselect("Select Teams", sorted(matches['team1'].unique()), default=['KKR', 'CSK', 'MI'])

filtered = matches[matches['season'].isin(seasons)]
if teams:
    filtered = filtered[(filtered['team1'].isin(teams)) | (filtered['team2'].isin(teams))]

# KPIs
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", len(filtered))
col2.metric("Total Runs", f"{deliveries['total_runs'].sum():,}")
col3.metric("Highest Total", f"{filtered['total_run_x'].max()}")
col4.metric("Most 6s Player", "Russell - 205") # You can calculate this

# Row 1 Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Matches Won by Team")
    wins = pd.concat([filtered['team1'], filtered['team2'], filtered['winner']])
    win_counts = filtered['winner'].value_counts().head(10).reset_index()
    win_counts.columns = ['Team', 'Wins']
    fig1 = px.bar(win_counts, x='Team', y='Wins', color='Wins', text='Wins')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Toss Decision vs Match Result")
    toss_win = filtered[filtered['toss_winner'] == filtered['winner']]
    toss_lose = filtered[filtered['toss_winner']!= filtered['winner']]
    fig2 = go.Figure(data=[
        go.Bar(name='Won Match', x=['Toss Won', 'Toss Lost'], y=[len(toss_win), len(toss_lose)]),
        go.Bar(name='Lost Match', x=['Toss Won', 'Toss Lost'], y=[len(filtered)-len(toss_win), len(filtered)-len(toss_lose)])
    ])
    fig2.update_layout(barmode='group')
    st.plotly_chart(fig2)

# Venue Analysis
st.subheader("Performance at Venues")
venue_stats = filtered.groupby('venue')['winner'].value_counts().unstack().fillna(0)
if teams:
    venue_stats = venue_stats[teams]
fig3 = px.imshow(venue_stats, text_auto=True, aspect="auto", color_continuous_scale='Blues')
st.plotly_chart(fig3)

# Top Players
st.subheader("Top Performers")
tab1, tab2 = st.tabs(["Top Batsmen", "Top Bowlers"])

with tab1:
    batsman_runs = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    fig4 = px.bar(batsman_runs, orientation='h', title="Most Runs")
    st.plotly_chart(fig4)

with tab2:
    bowlers = deliveries[deliveries['is_wicket']==1].groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(10)
    fig5 = px.bar(bowlers, orientation='h', title="Most Wickets")
    st.plotly_chart(fig5)

# Insights
st.subheader("🔍 Auto Insights")
best_venue = venue_stats.sum(axis=1).idxmax()
chasing_wins = len(filtered[filtered['win_by_runs']==0])
defending_wins = len(filtered[filtered['win_by_wickets']==0])

st.write(f"1. **Highest Scoring Venue**: {best_venue}")
st.write(f"2. **Chasing Teams Win**: {chasing_wins/len(filtered)*100:.1f}% of matches")
st.write(f"3. **Toss Impact**: Teams winning toss win {len(toss_win)/len(filtered)*100:.1f}% matches")

st.download_button("Download Filtered Data", filtered.to_csv(index=False).encode(), "ipl_filtered.csv")



pip install streamlit plotly pandas
streamlit run ipl_dashboard.py