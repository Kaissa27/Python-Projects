import pandas as pd
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_single_term(term, index):
    """The task handler assigned to each parallel worker thread."""
    print(f"🚀 Worker activated for row {index + 1}: '{term}'")
    
    # Each thread must open its own isolated browser context
    with sync_playwright() as p:
        # Launching in headless mode is mandatory for heavy parallel work
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto("https://www.wikipedia.org/")
            page.fill("input#searchInput", term)
            page.press("input#searchInput", "Enter")
            
            # Dynamic async element wait gate
            page.wait_for_selector("div.mw-content-ltr p")
            first_paragraph = page.locator("div.mw-content-ltr p").first.inner_text()
            summary = first_paragraph[:150] + "..." if len(first_paragraph) > 150 else first_paragraph
            status = "Success"
        except Exception as e:
            summary = "Extraction failed during parallel execution"
            status = f"Failed: {str(e)[:50]}"
        finally:
            context.close()
            browser.close()
            
    return {
        "SearchTerm": term,
        "WebSummary": summary,
        "AuditStatus": status,
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def run_parallel_pipeline():
    start_time = time.time()
    
    # 1. Load data sheet
    df = pd.read_csv("search_queries.csv")
    search_tasks = list(df["SearchTerm"])
    
    results = []
    
    # 2. Initialize the Thread Pool Executor
    # max_workers=3 means up to 3 browsers will run completely simultaneously
    print(f"📦 Initializing Parallel Engine Pool with 3 active browser slots...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        
        # Submit all items to the queue dynamically
        futures = {
            executor.submit(process_single_term, term, i): i 
            for i, term in enumerate(search_tasks)
        }
        
        # 3. Harvest outputs out of order as soon as they finish processing
        for future in as_completed(futures):
            row_index = futures[future]
            try:
                data_row = future.result()
                results.append(data_row)
                print(f"✅ Row {row_index + 1} finalized and returned to core coordinator.")
            except Exception as exc:
                print(f"❌ Thread execution exception at row {row_index + 1}: {exc}")

    # 4. Consolidate results into unified spreadsheet
    output_df = pd.DataFrame(results)
    output_df.to_csv("parallel_audit_output.csv", index=False)
    
    total_time = time.time() - start_time
    print(f"\n🏁 Parallel Pipeline Complete in {total_time:.2f} seconds!")

if __name__ == "__main__":
    run_parallel_pipeline()
