import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def run_multivariate_pipeline():
    print("🚀 Initializing Multivariate Data Science Pipeline...")
    
    # 1. DATA ENGINEERING LAYER (Simulating a complex corporate matrix)
    np.random.seed(42)
    n_months = 120
    
    marketing_spend = np.random.uniform(20, 500, n_months)      # Feature 1: Budget in $K
    support_team_size = np.random.randint(5, 30, n_months)      # Feature 2: Team headcount
    # Feature 3: Categorical Season variable (Text)
    seasons = np.random.choice(['Winter', 'Spring', 'Summer', 'Autumn'], n_months)
    
    # Target Variable: Revenue driven by all three components plus some market noise
    season_boost = np.where(seasons == 'Winter', 150.0, 20.0)   # Winter holiday revenue surge
    gross_revenue = 100 + (2.1 * marketing_spend) + (5.5 * support_team_size) + season_boost + np.random.normal(0, 30, n_months)

    # Consolidate raw data arrays into a Pandas DataFrame
    df = pd.DataFrame({
        "Marketing_Spend_K": marketing_spend,
        "Support_Team_Size": support_team_size,
        "Season": seasons,
        "Gross_Revenue_K": gross_revenue
    })
    
    print("📋 RAW FEATURE MATRIX SAMPLE (First 3 rows):")
    print(df.head(3), "\n")

    # 2. TRANSFORMATION PHASE: ONE-HOT ENCODING
    # Machine learning models don't understand the string "Winter". 
    # pd.get_dummies converts text into binary columns (e.g., Season_Winter = 1 or 0)
    df_encoded = pd.get_dummies(df, columns=["Season"], drop_first=True)
    
    print("🧼 ENCODED FEATURE MATRIX SAMPLE (Text transformed to binary bits):")
    print(df_encoded.head(3), "\n")

    # 3. MATRIX SEPARATION & TRAIN-TEST SPLITTING
    # Separate our features (inputs) from our target variable (revenue output)
    X = df_encoded.drop(columns=["Gross_Revenue_K"])
    y = df_encoded["Gross_Revenue_K"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. MULTIVARIATE MODEL TRAINING
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5. COEFFICIENT COEFFICIENT ANALYSIS (Deconstructing the Business Drivers)
    print("📊 EXTRACTED MATHEMATICAL COEFFICIENTS:")
    print(f"🔹 Baseline (Intercept): ${model.intercept_:.2f}K")
    for feature, coef in zip(X.columns, model.coef_):
        print(f"   • {feature:<25} Weight: {coef:>6.2f}")

    # 6. EVALUATION MATRIX
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"\n🎯 MODEL PERFORMANCE STATUS:")
    print(f"   • R² Accuracy Score: {r2:.2f} (Explains {r2*100:.1f}% of data variance)")
    print(f"   • Root Mean Squared Error (RMSE): ${rmse:.2f}K")

    # 7. PRODUCTION FORECAST SIMULATION
    # What if next month we spend $200K on marketing, have 15 support staff, and it's Winter?
    # The feature matrix format must match X exactly: Marketing, Support, Season_Spring, Season_Summer, Season_Winter
    # For a Winter row: Season_Spring=0, Season_Summer=0, Season_Winter=1
    future_scenario = pd.DataFrame([[200.0, 15, 0, 0, 1]], columns=X.columns)
    prediction = model.predict(future_scenario)
    print(f"\n🔮 ENTERPRISE FORECAST PROJECTION: Projected Revenue is **${prediction[0]:.2f}K**.")

if __name__ == "__main__":
    run_multivariate_pipeline()
