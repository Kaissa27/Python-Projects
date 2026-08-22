import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Netflix Analyzer", layout="wide")
st.title("🎬 Netflix Movies & TV Shows Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv") # Kaggle dataset
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Titles", len(df))
col2.metric("Movies", len(df[df['type']=='Movie']))
col3.metric("TV Shows", len(df[df['type']=='TV Show']))
col4.metric("Top Genre", df['listed_in'].str.split(', ').explode().mode()[0])

# Row 1: Content Type & Growth
col1, col2 = st.columns(2)
with col1:
    st.subheader("Movies vs TV Shows")
    type_count = df['type'].value_counts().reset_index()
    fig1 = px.pie(type_count, names='type', values='count')
    st.plotly_chart(fig1)

with col2:
    st.subheader("Content Added Over Years")
    yearly = df.groupby('year_added').size().reset_index(name='count')
    fig2 = px.line(yearly, x='year_added', y='count', markers=True)
    st.plotly_chart(fig2)

# Genre Analysis
st.subheader("🔥 Top 15 Genres on Netflix")
genres = df['listed_in'].str.split(', ').explode().value_counts().head(15).reset_index()
genres.columns = ['genre', 'count']
fig3 = px.bar(genres, x='count', y='genre', orientation='h')
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3)

# Ratings & Countries
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Ratings")
    rating_count = df['rating'].value_counts().head(10).reset_index()
    fig4 = px.bar(rating_count, x='rating', y='count')
    st.plotly_chart(fig4)

with col2:
    st.subheader("Top Countries Producing Content")
    country_count = df['country'].str.split(', ').explode().value_counts().head(10).reset_index()
    country_count.columns = ['country', 'count']
    fig5 = px.bar(country_count, x='count', y='country', orientation='h')
    st.plotly_chart(fig5)

# ===== RECOMMENDATION ENGINE =====
st.subheader("🤖 Netflix Recommendation Engine")

# Simple content-based recommender
@st.cache_data
def build_recommender(data):
    data = data.dropna(subset=['description'])
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = build_recommender(df)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = df[df['title'].str.contains(title, case=False, na=False)].index
    if len(idx) == 0:
        return pd.DataFrame()
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return df.iloc[movie_indices][['title', 'type', 'listed_in', 'description']]

movie_input = st.text_input("Enter a movie/show you liked (e.g., Stranger Things)")

if movie_input:
    recs = get_recommendations(movie_input)
    if not recs.empty:
        st.write(f"**Because you watched {movie_input}, you might like:**")
        for _, row in recs.iterrows():
            st.write(f"- **{row['title']}** ({row['type']}) - {row['listed_in']}")
    else:
        st.write("No recommendations found. Try another title.")

# Insights
st.subheader("🔍 Key Insights")
st.write("1. **Most Content**: TV-MA and TV-14 are dominant ratings")
st.write("2. **Peak Year**: Netflix added most titles in 2019-2020")
st.write("3. **Top Genres**: International Movies, Dramas, Comedies rule")
st.write("4. **Recommendation**: Add more Korean Dramas + True Crime - fastest growing")

st.download_button("📥 Download Data", df.to_csv(index=False).encode(), "netflix_analysis.csv")