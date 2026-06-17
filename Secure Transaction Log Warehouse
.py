import sqlite3
from datetime import datetime

class FinancialWarehouse:
    def __init__(self, db_name="ledger.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_tag TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')

    def log_asset(self, asset_tag: str, value: float):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ledger (asset_tag, value, timestamp) VALUES (?, ?, ?)",
                (asset_tag, value, timestamp)
            )
            conn.commit()

    def generate_aggregate_report(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT asset_tag, SUM(value), COUNT(*) FROM ledger GROUP BY asset_tag")
            return cursor.fetchall()

if __name__ == "__main__":
    db = FinancialWarehouse()
    db.log_asset("EQUITY_AAPL", 1500.45)
    db.log_asset("CASH_USD", 5000.00)
    db.log_asset("EQUITY_AAPL", 300.12)
    
    print("\n--- 📊 DATA WAREHOUSE AGGREGATE REPORT ---")
    for asset, total, count in db.generate_aggregate_report():
        print(f"🔹 Asset: {asset:<15} Total Value: ${total:>10,.2f} [Entries: {count}]")
