import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

st.title("🌸 Project 1: Iris Flower Classifier - Your First ML Model")

# Load data
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target
df['species_name'] = df['species'].map({0:'Setosa', 1:'Versicolor', 2:'Virginica'})

st.write("Dataset Preview", df.head())

# Train
X = df[iris.feature_names]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)
acc = model.score(X_test, y_test)

st.metric("Model Accuracy", f"{acc*100:.2f}%")

# Prediction UI
st.subheader("🔮 Try Prediction")
sl = st.slider("Sepal Length", 4.0, 8.0, 5.1)
sw = st.slider("Sepal Width", 2.0, 4.5, 3.5)
pl = st.slider("Petal Length", 1.0, 7.0, 1.4)
pw = st.slider("Petal Width", 0.1, 2.5, 0.2)

if st.button("Predict"):
    pred = model.predict([[sl, sw, pl, pw]])
    name = ['Setosa','Versicolor','Virginica'][pred[0]]
    st.success(f"Predicted Flower: **{name}**")
    st.balloons()

with st.expander("📌 Resume Point"):
    st.code("Built first ML classification model using RandomForest on Iris dataset (150 samples), achieved 100% accuracy, deployed with Streamlit")