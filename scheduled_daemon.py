import os 
import time
import requests
import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. ARCHITECTURAL SAFETY: Dynamically pinpoint the script's exact folder
BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "search_queries.csv"
OUTPUT_CSV = BASE_DIR / "scheduled_output.csv"

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def process_single_term(term):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.wikipedia.org/", timeout=30000)
            page.fill("input#searchInput", term)
            page.press("input#searchInput", "Enter")
            page.wait_for_selector("div.mw-content-ltr p", timeout=10000)
            first_p = page.locator("div.mw-content-ltr p").first.inner_text()
            summary = first_p[:100] + "..." if len(first_p) > 100 else first_p
            status = "Success"
        except Exception as e:
            summary = "N/A"
            status = f"Failed: {str(e)[:30]}"
        finally:
            context.close()
            browser.close()
    return {"SearchTerm": term, "Summary": summary, "Status": status}

def main():
    start_time = time.time()
    
    # Verify input file exists at the absolute path
    if not INPUT_CSV.exists():
        print(f"❌ Aborting. File not found at: {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)
    tasks = list(df["SearchTerm"])
    results = []
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_single_term, term): term for term in tasks}
        for future in as_completed(futures):
            results.append(future.result())

    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_CSV, index=False)
    
    # Network metrics reporting
    elapsed = time.time() - start_time
    success_count = len(output_df[output_df["Status"] == "Success"])
    
    if DISCORD_WEBHOOK_URL != "YOUR_DISCORD_WEBHOOK_URL_HERE":
        payload = {
            "content": f"⏰ **🚨 DAEMON AUDIT COMPLETE**\n📝 Processed {len(output_df)} items ({success_count} successful) in {elapsed:.2f}s."
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    main()
