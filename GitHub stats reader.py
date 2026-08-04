import streamlit as st
import requests
import plotly.express as px

st.title("📊 GitHub Profile Generator")

username = st.text_input("Enter GitHub Username")

def get_github_data(user):
    url = f"https://api.github.com/users/{user}"
    repos_url = f"https://api.github.com/users/{user}/repos"
    
    user_data = requests.get(url).json()
    repos = requests.get(repos_url).json()
    
    # Get language stats
    languages = {}
    for repo in repos:
        if 'language' in repo and repo['language']:
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    
    return user_data, languages, len(repos)

if st.button("Generate Profile"):
    user_data, languages, repo_count = get_github_data(username)
    
    col1, col2, col3 = st.columns(3