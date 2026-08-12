import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re
import requests
from newspaper import Article

# Sample training data - you can expand this
# In real project, download: "Fake and Real News Dataset" from Kaggle
DATA = {
    'text': [
        'Government announces new policy to help farmers with subsidies',
        'Breaking: Scientists discover cure for all diseases in 24 hours',
        'India wins cricket match against Australia in final over',
        'Celebrity dies twice in one week, doctors shocked',
        'New metro line opens in Kolkata, reduces travel time',
        'NASA confirms aliens living in moon, hiding from humans'
    ],
    'label': [0, 1, 0, 1, 0, 1] # 0=Real, 1=Fake
}

df = pd.DataFrame(DATA)

# Train simple model
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
    ('clf', LogisticRegression())
])
model.fit(df['text'], df['label'])

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA