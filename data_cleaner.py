import pandas as pd
import numpy as np

def run_data_normalization():
    # Simulated dirty dataset (Notice the missing 'None' and NaN markers)
    raw_telemetry_logs = {
        "DeviceID": ["Node_A", "Node_B", "Node_A", "Node_C", "Node_B"],
        "Temperature": [42.5, np.nan, 41.2, 99.0, 43.0], 
        "Status": ["Active", "Offline", "Active", "CRITICAL", "Active"],
        "RequestsProcessed": [1200, 0, 1200, np.nan, 850]
    }

    # 1. Instantiate the structured Vectorized Matrix (DataFrame)
    df = pd.DataFrame(raw_telemetry_logs)
    print("📋 RAW UNSTRUCTURED MATRIX:")
    print(df, "\n")

    # 2. Drop absolute identical data blocks (Deduplication)
    df = df.drop_duplicates()

    # 3. Handle Null vectors using statistical interpolation (Imputation)
    mean_temp = df["Temperature"].mean()
    df["Temperature"] = df["Temperature"].fillna(mean_temp)
    
    # Fill remaining missing integers with a default zero baseline state
    df["RequestsProcessed"] = df["RequestsProcessed"].fillna(0).astype(int)

    # 4. Outlier Filtering (Eliminating bad anomalies)
    # Exclude system readings that exceed unrealistic operational bounds
    df = df[df["Temperature"] < 90.0]

    print("✅ NORMALIZED CLEAN DATA FRAME:")
    print(df)
    
    # Export clean data warehouse matrix
    df.to_csv("clean_telemetry.csv", index=False)

if __name__ == "__main__":
    run_data_normalization()
