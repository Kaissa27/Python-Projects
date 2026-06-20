import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "enterprise_warehouse.db"

# =====================================================================
# 1. DATA WAREHOUSE SEEDING (Simulating real corporate tables)
# =====================================================================
def seed_production_database():
    """Generates mock production database tables to simulate real data analysis pools."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_transactions (
                transaction_id TEXT PRIMARY KEY,
                user_tier TEXT,
                revenue REAL,
                region TEXT
            )
        ''')
        
        # Insert raw transaction data blocks if table is empty
        cursor.execute("SELECT COUNT(*) FROM server_transactions")
        if cursor.fetchone()[0] == 0:
            mock_data = [
                ('TX101', 'Premium', 450.00, 'US-East'),
                ('TX102', 'Free', 0.00, 'US-West'),
                ('TX103', 'Premium', 1200.50, 'EU-West'),
                ('TX104', 'Standard', 150.00, 'US-East'),
                ('TX105', 'Premium', 890.00, 'US-West'),
                ('TX106', 'Standard', 150.00, 'EU-West'),
                ('TX107', 'Free', 0.00, 'US-East')
            ]
            cursor.executemany("INSERT INTO server_transactions VALUES (?, ?, ?, ?)", mock_data)
            conn.commit()
            print("💾 Production database seeded with raw transaction records.")

# =====================================================================
# 2. THE PIPELINE EXECUTION (Extract, Query & Analyze)
# =====================================================================
def run_sql_analytics_pipeline():
    seed_production_database()
    
    # Connect directly to the data infrastructure layer
    with sqlite3.connect(DB_FILE) as conn:
        print("🔌 Connection established. Executing analytical query extraction...")
        
        # We filter out 'Free' users directly at the database level to optimize memory bandwidth
        sql_query = """
            SELECT user_tier, region, revenue 
            FROM server_transactions 
            WHERE revenue > 0
        """
        
        # Pull live query results directly into a structured Pandas DataFrame matrix
        df = pd.read_sql_query(sql_query, conn)

    print("\n📥 EXTRACTED TARGET DATAFRAME MATRIX:")
    print(df, "\n")

    # 3. COMPUTATIONAL ANALYTICS MATRIX (The Transformation Phase)
    # Pivot the data to find total revenue grouped by Region and User Tier simultaneously
    analysis_pivot = df.groupby(["region", "user_tier"])["revenue"].sum().reset_index()
    
    print("📈 CALCULATED ANALYTICS INTERPOLATION MATRIX:")
    print(analysis_pivot)

    # 4. DATA LOADING STORAGE (Archiving results back to SQL)
    with sqlite3.connect(DB_FILE) as conn:
        # Load the newly processed analytical matrices straight back into a unique archive table
        analysis_pivot.to_sql("archived_regional_revenue", conn, if_exists="replace", index=False)
        print("\n🏁 Aggregated data successfully loaded back into database table: [archived_regional_revenue]")

if __name__ == "__main__":
    run_sql_analytics_pipeline()
