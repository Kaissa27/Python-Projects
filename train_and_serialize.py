import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "revenue_model.pkl"

def export_trained_model():
    # 1. Generate historical corporate training matrix
    np.random.seed(42)
    n_months = 100
    marketing = np.random.uniform(20, 500, n_months)
    support = np.random.randint(5, 30, n_months)
    
    # Simple binary indicator for Winter holiday surge (1 = Winter, 0 = Other)
    is_winter = np.random.choice([0, 1], n_months)
    
    # Calculate target revenue matrix
    gross_revenue = 100 + (2.1 * marketing) + (5.5 * support) + (150.0 * is_winter) + np.random.normal(0, 10, n_months)

    df = pd.DataFrame({
        "Marketing_Spend_K": marketing,
        "Support_Team_Size": support,
        "Is_Winter": is_winter,
        "Gross_Revenue_K": gross_revenue
    })

    # 2. Split Features and Target Vector
    X = df[["Marketing_Spend_K", "Support_Team_Size", "Is_Winter"]]
    y = df["Gross_Revenue_K"]

    # 3. Train Model Weights
    model = LinearRegression()
    model.fit(X, y)
    print(f"✅ Model trained successfully. R² Score: {model.score(X, y):.2f}")

    # 4. SERIALIZATION: Freeze and save the model file to disk
    joblib.dump(model, MODEL_FILE)
    print(f"💾 Model mathematical weights saved permanently to: {MODEL_FILE}")

if __name__ == "__main__":
    export_trained_model()
