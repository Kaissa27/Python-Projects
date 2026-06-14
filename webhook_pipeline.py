import pandas as pd
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time

# ENTER YOUR LIVE DISCORD WEBHOOK LINK HERE TO TEST NETWORK OUTPUT
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def process_single_term(term, index):
    """Parallel worker task handler."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto("https://www.wikipedia.org/")
            page.fill("input#searchInput", term)
            page.press("input#searchInput", "Enter")
            
            page.wait_for_selector("div.mw-content-ltr p")
            first_paragraph = page.locator("div.mw-content-ltr p").first.inner_text()
            summary = first_paragraph[:100] + "..." if len(first_paragraph) > 100 else first_paragraph
            status = "Success"
        except Exception:
            summary = "N/A"
            status = "Failed"
        finally:
            context.close()
            browser.close()
            
    return {"SearchTerm": term, "Summary": summary, "Status": status}

def dispatch_webhook_report(total_items, success_count, fail_count, elapsed_time):
    """Assembles a structured JSON payload and ships it over the web network."""
    if DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("\n⚠️ Webhook dispatch skipped: Please provide a valid URL to transmit reports.")
        return

    # Constructing a rich message using Discord's markdown format
    payload = {
        "content": (
            f"📊 **AUTOMATION PIPELINE REPORT**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏁 **Status:** Complete\n"
            f"⏱️ **Execution Time:** {elapsed_time:.2f} seconds\n"
            f"📦 **Total Tasks Audited:** {total_items}\n"
            f"✅ **Successful Extractions:** {success_count}\n"
            f"❌ **Failed Extractions:** {fail_count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔔 *This is an automated server message. No response required.*"
        )
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("🚀 Report successfully dispatched and displayed in the remote chat workspace!")
        else:
            print(f"❌ Webhook returned network error code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Network transmission failure: {e}")

def run_pipeline():
    start_time = time.time()
    
    # 1. Gather tasks
    df = pd.read_csv("search_queries.csv")
    search_tasks = list(df["SearchTerm"])
    results = []
    
    print("📦 Booting parallel worker channels...")
    # 2. Run workers concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_single_term, term, i): term for i, term in enumerate(search_tasks)}
        for future in as_completed(futures):
            results.append(future.result())

    # 3. Analyze output metrics via Pandas
    output_df = pd.DataFrame(results)
    output_df.to_csv("monitored_output.csv", index=False)
    
    total_items = len(output_df)
    success_count = len(output_df[output_df["Status"] == "Success"])
    fail_count = len(output_df[output_df["Status"] == "Failed"])
    elapsed_time = time.time() - start_time

    # 4. Trigger the network alert system
    dispatch_webhook_report(total_items, success_count, fail_count, elapsed_time)

if __name__ == "__main__":
    run_pipeline()
