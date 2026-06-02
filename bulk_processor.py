import pandas as pd
from playwright.sync_api import sync_playwright
import time

def run_bulk_data_pipeline():
    # 1. Read the input spreadsheet using Pandas
    try:
        input_df = pd.read_csv("search_queries.csv")
    except FileNotFoundError:
        print("Error: 'search_queries.csv' not found. Please run Step 1 first.")
        return

    results_list = []

    # 2. Launch the underlying browser engine
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Headless mode for rapid server processing
        context = browser.new_context()
        page = context.new_page()

        print(f"🚀 Starting bulk pipeline. Processing {len(input_df)} records...")

        # 3. Loop through every row in the spreadsheet data frame
        for index, row in input_df.iterrows():
            term = row['SearchTerm']
            print(f"🔍 [Row {index + 1}] Processing Web Query: '{term}'")

            try:
                # Navigate to the search landing pad
                page.goto("https://www.wikipedia.org/")
                page.fill("input#searchInput", term)
                page.press("input#searchInput", "Enter")

                # Wait dynamically for the article page layout to resolve
                page.wait_for_selector("div.mw-content-ltr p")
                
                # Extract the text from the first descriptive paragraph
                first_paragraph = page.locator("div.mw-content-ltr p").first.inner_text()
                
                # Truncate text if it's too long for a clean spreadsheet cell
                summary = first_paragraph[:150] + "..." if len(first_paragraph) > 150 else first_paragraph
                status = "Success"

            except Exception as e:
                summary = "Could not extract text summary content"
                status = f"Failed: {str(e)[:50]}"

            # 4. Append row outputs dynamically to our local memory dictionary
            results_list.append({
                "SearchTerm": term,
                "WebSummary": summary,
                "AuditStatus": status,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        # Close out our active web network ports
        context.close()
        browser.close()

    # 5. Convert results back into a Pandas DataFrame and export to a master sheet
    output_df = pd.DataFrame(results_list)
    output_df.to_csv("audit_results_output.csv", index=False)
    print("\n🏁 Master Data Export Complete! Check 'audit_results_output.csv'.")

if __name__ == "__main__":
    run_bulk_data_pipeline()
