import sqlite3
import time
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Data Pipeline Core API")

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "production_analytics.db"

# Schema Validation: Defines exactly what fields incoming network data must have
class AuditRecord(BaseModel):
    search_term: str
    char_count: int
    status: str

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS web_audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT NOT NULL,
                char_count INTEGER NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

@app.on_event("startup")
def on_startup():
    init_db()

# =====================================================================
# 1. THE DATA INGESTION ENDPOINT (Used by Automation Workers)
# =====================================================================
@app.post("/logs", status_code=201)
def log_execution(record: AuditRecord):
    """Receives pipeline metrics across the network and writes them to SQL."""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO web_audit_logs (search_term, char_count, status, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (record.search_term, record.char_count, record.status, timestamp))
            conn.commit()
        return {"status": "success", "message": "Telemetry matrix recorded."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failure: {str(e)}")

# =====================================================================
# 2. THE ANALYTICS SERVICE ENDPOINT (Used by the Web Dashboard)
# =====================================================================
@app.get("/logs")
def get_all_logs():
    """Fetches full database ledger records and delivers them as JSON over HTTP."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            df = pd.read_sql_query("SELECT * FROM web_audit_logs ORDER BY timestamp DESC", conn)
        # Convert the pandas data frame to a standard web-friendly JSON format
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database read failure: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Launch backend server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
