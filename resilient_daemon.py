import os
import time
import logging
import requests
import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. SETUP STRUCTURED LOGGING ENGINE
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "pipeline.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Thread-%(thread)d) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

INPUT_CSV = BASE_DIR / "search_queries.csv"
OUTPUT_CSV = BASE_DIR / "resilient_output.csv"
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def process_term_with_retry(term, max_retries=3):
    """Executes browser automation with an exponential backoff retry policy."""
    retries = 0
    delay = 2  # Starting delay in seconds
    
    while retries < max_retries:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                logging.info(f"Initiating audit for query: '{term}' (Attempt {retries + 1}/{max_retries})")
                page.goto("https://www.wikipedia.org/", timeout=15000)
                page.fill("input#searchInput", term)
                page.press("input#searchInput", "Enter")
                
                page.wait_for_selector("div.mw-content-ltr p", timeout=5000)
                first_p = page.locator("div.mw-content-ltr p").first.inner_text()
                
                summary = first_p[:100] + "..." if len(first_p) > 100 else first_p
                logging.info(f"Successfully extracted data for query: '{term}'")
                return {"SearchTerm": term, "Summary": summary, "Status": "Success"}
                
            except Exception as e:
                retries += 1
                logging.warning(f"Attempt {retries} failed for '{term}'. Error: {str(e)[:40]}")
                
                if retries < max_retries:
                    logging.info(f"Sleeping for {delay}s before retry path optimization...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff multiplier
                else:
                    logging.error(f"Critical Exhaustion. All retries failed for query: '{term}'")
            finally:
                context.close()
                browser.close()
                
    return {"SearchTerm": term, "Summary": "N/A", "Status": f"Failed after {max_retries} attempts"}

def main():
    logging.info("=== CORE PIPELINE DAEMON ACTIVATED ===")
    start_time = time.time()
    
    if not INPUT_CSV.exists():
        logging.critical(f"Execution halted. Target input vector missing at: {INPUT_CSV}")
        return

    try:
        df = pd.read_csv(INPUT_CSV)
        tasks = list(df["SearchTerm"])
        results = []
        
        logging.info(f"Spreadsheet parsed successfully. Distributing {len(tasks)} tasks across Thread Pool.")
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(process_term_with_retry, term): term for term in tasks}
            for future in as_completed(futures):
                results.append(future.result())

        output_df = pd.DataFrame(results)
        output_df.to_csv(OUTPUT_CSV, index=False)
        
        elapsed = time.time() - start_time
        success_count = len(output_df[output_df["Status"] == "Success"])
        logging.info(f"Pipeline executed successfully. {success_count}/{len(output_df)} passed in {elapsed:.2f}s.")
        
    except Exception as e:
        logging.critical(f"Fatal crash inside pipeline main coordinator loop: {e}")

if __name__ == "__main__":
    main() 
