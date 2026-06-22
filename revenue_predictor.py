import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def run_predictive_pipeline():
    print("🚀 Initializing Predictive Machine Learning Pipeline...")
    
    # 1. DATA GENERATION LAYER (Simulating historic corporate metric data)
    # Let's say we are tracking 100 historical months of corporate operations
    np.random.seed(42)
    marketing_spend = np.random.uniform(10, 500, 100) # In thousands of dollars
    # Gross Revenue has a baseline, a direct link to marketing, and random market noise
    gross_revenue = 50 + (2.5 * marketing_spend) + np.random.normal(0, 75, 100)

    # Pack our vectors into a structured Pandas dataframe matrix
    df = pd.DataFrame({
        "Marketing_Spend_K": marketing_spend,
        "Gross_Revenue_K": gross_revenue
    })

    # 2. FEATURE ENGINEERING & MATRIX SPLITTING
    # X (Features/Inputs) must be a 2D matrix; y (Target/Output) is a 1D vector
    X = df[["Marketing_Spend_K"]]
    y = df["Gross_Revenue_K"]

    # Split data: 80% to train the model, 20% held back to test its predictive accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. MODEL TRAINING PHASE (Linear Regression Algorithm)
    model = LinearRegression()
    model.fit(X_train, y_train) # The computer calculates the mathematical weights here
    
    print(f"📈 Model Training Complete. Baseline Revenue: ${model.intercept_:.2f}K")
    print(f"📊 Weight Coefficient: For every $1K spent, revenue rises by ${model.coef_[0]:.2f}K")

    # 4. EVALUATION & TESTING MATRIX
    # Ask the trained model to predict values on our unseen test dataset
    y_pred = model.predict(X_test)

    # Calculate statistical performance markers
    r2 = r2_score(y_test, y_pred) # Coefficient of determination (Max 1.0)
    print(f"🎯 Model Accuracy Variance (R² Score): {r2:.2f}")

    # 5. FORECASTING FUTURE SCENARIOS (Predicting the Unknown)
    # What happens if executive leadership allocates $350K to marketing next month?
    future_spend = np.array([[350.0]])
    predicted_return = model.predict(future_spend)
    print(f"\n🔮 FUTURE FORECAST: A spend of $350K is projected to capture **${predicted_return[0]:.2f}K** in Gross Revenue.")

    # 6. GRAPHICAL PRESENTATION ENGINE
    plt.figure(figsize=(8, 5))
    # Plot our real training data points
    plt.scatter(X_train, y_train, color="#34495e", alpha=0.6, label="Historic Monthly Data")
    # Plot the machine learning algorithm's line of best fit
    plt.plot(X_test, y_pred, color="#e74c3c", linewidth=3, label="Model Prediction Vector")
    
    plt.title("Predictive Analytics Matrix: Revenue Forecast vs Marketing Allocation")
    plt.xlabel("Marketing Allocation Budget ($ in Thousands)")
    plt.ylabel("Gross Revenue Yield ($ in Thousands)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.savefig("predictive_revenue_model.png", dpi=300)
    plt.close()
    print("💾 Predictive visual analysis chart successfully saved to disk as 'predictive_revenue_model.png'")

if __name__ == "__main__":
    run_predictive_pipeline()
