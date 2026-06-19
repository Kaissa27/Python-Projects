import pandas as pd

def compute_business_intelligence():
    # Transaction stream source
    ledger_records = {
        "Branch": ["North", "South", "East", "North", "South", "East", "North"],
        "Category": ["Tech", "Office", "Tech", "Furniture", "Office", "Furniture", "Tech"],
        "SaleAmount": [1500, 450, 1200, 3100, 500, 890, 950]
    }

    df = pd.DataFrame(ledger_records)

    # 1. Compute multi-variable statistical groupings
    grouped_report = df.groupby(["Branch", "Category"]).agg(
        Total_Revenue=("SaleAmount", "sum"),
        Average_Ticket_Size=("SaleAmount", "mean"),
        Transaction_Volume=("SaleAmount", "count")
    ).reset_index()

    print("📊 MULTI-DIMENSIONAL BUSINESS INTELLIGENCE MATRIX:")
    print(grouped_report.to_string(index=False))

if __name__ == "__main__":
    compute_business_intelligence()
