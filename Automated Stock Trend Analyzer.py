def analyze_market_data():
    # Simulated daily closing prices for "TECH_CORP" over 10 days
    prices = [150.25, 152.10, 148.50, 147.00, 149.30, 155.40, 158.20, 157.00, 160.10, 162.50]
    
    # Configuration
    window_size = 3  # We want to look at 3-day averages
    print(f"--- Market Analytics: 10-Day Trend Report ---")
    print(f"Initial Price: ${prices[0]} | Current Price: ${prices[-1]}")
    print("-" * 45)

    # 1. Calculating Moving Averages (Slicing)
    # A moving average "smooths out" price spikes to show the true trend
    moving_averages = []
    for i in range(len(prices) - window_size + 1):
        window = prices[i : i + window_size]
        avg = sum(window) / window_size
        moving_averages.append(round(avg, 2))

    # 2. Calculating Daily Volatility (Difference between Max and Min)
    volatility = max(prices) - min(prices)

    # 3. Trend Detection (Percentage Change)
    start_price = prices[0]
    end_price = prices[-1]
    percent_change = ((end_price - start_price) / start_price) * 100

    # 4. Generating Automated "Action" Signals
    print(f"Moving Averages (3-Day): {moving_averages}")
    print(f"Total Volatility:        ${volatility:.2f}")
    print(f"Overall Performance:     {percent_change:+.2f}%")

    if percent_change > 5:
        signal = "🚀 BULLISH (Strong Buy)"
    elif percent_change < -5:
        signal = "📉 BEARISH (Strong Sell)"
    else:
        signal = "↔️ NEUTRAL (Hold)"

    print(f"\n[ANALYSIS RESULT]: {signal}")

if __name__ == "__main__":
    analyze_market_data()