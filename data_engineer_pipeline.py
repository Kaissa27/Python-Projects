import sqlite3 
import time
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "production_analytics.db"
CHART_FILE = BASE_DIR / "execution_dashboard.png"

# =====================================================================
# 1. DATABASE INITIALIZATION (The Load Layer)
# =====================================================================
def init_database():
    """Sets up the relational table structure to archive pipeline data."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT NOT NULL,
                char_count INTEGER NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

# =====================================================================
# 2. PARALLEL WORKER ENGINE (The Extract Layer)
# =====================================================================
def extract_web_data(term):
    """Headless worker gathering raw web metrics."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.wikipedia.org/", timeout=15000)
            page.fill("input#searchInput", term)
            page.press("input#searchInput", "Enter")
            page.wait_for_selector("div.mw-content-ltr p", timeout=5000)
            
            raw_text = page.locator("div.mw-content-ltr p").first.inner_text()
            char_count = len(raw_text)
            status = "Success"
        except Exception:
            char_count = 0
            status = "Failed"
        finally:
            context.close()
            browser.close()
            
    return {"search_term": term, "char_count": char_count, "status": status}

# =====================================================================
# 3. METRIC VISUALIZATION ENGINE (The Analytics Layer)
# =====================================================================
def generate_visual_dashboard():
    """Reads transactional SQL data back into Pandas to construct an image graph."""
    with sqlite3.connect(DB_FILE) as conn:
        # Read directly from SQL table straight into a Pandas DataFrame
        df = pd.read_sql_query("SELECT status, COUNT(*) as count FROM web_audit_logs GROUP BY status", conn)
        
    # Generate a visual bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(df['status'], df['count'], color=['#2ecc71', '#e74c3c'])
    plt.title('Automation Performance Vector')
    plt.xlabel('Execution Outcome')
    plt.ylabel('Total Runs Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the chart to disk as an image asset
    plt.savefig(CHART_FILE)
    plt.close()
    print(f"📊 Live telemetry chart updated and exported to: {CHART_FILE}")

# =====================================================================
# 4. ORCHESTRATION PIPELINE (The Transform & Coordinate Layer)
# =====================================================================
def run_pipeline():
    init_database()
    
    # Target search vectors (Normally extracted from an upstream database or API)
    targets = ["Python (programming language)", "Data engineering", "Automation", "InvalidPageXYZ999"]
    raw_extracted_batches = []
    
    print("🚀 Commencing concurrent ETL pipeline matrix...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(extract_web_data, term) for term in targets]
        for future in as_completed(futures):
            raw_extracted_batches.append(future.result())
            
    # Transform: Parse list data into a pandas structure and format metrics
    df_transformed = pd.DataFrame(raw_extracted_batches)
    df_transformed["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Load: Bulk insert the cleaned pandas frame right into the SQLite database table
    with sqlite3.connect(DB_FILE) as conn:
        df_transformed.to_sql("web_audit_logs", conn, if_exists="append", index=False)
    print("💾 Data transaction batches finalized and written permanently to SQL database.")
    
    # Analyze: Trigger dashboard generation
    generate_visual_dashboard()

if __name__ == "__main__":
    run_pipeline()
