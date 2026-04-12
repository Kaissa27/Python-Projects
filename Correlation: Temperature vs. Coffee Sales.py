def analyze_weather_impact():
    # Dataset 1: Average Daily Temperature (°C)
    # Dataset 2: Total Coffee Sales (Units)
    # Both lists are mapped by index (Day 1, Day 2, etc.)
    temp_data = [5, 8, 12, 15, 22, 28, 32, 35, 30, 25]
    sale_data = [120, 110, 95, 80, 60, 45, 30, 25, 35, 55]

    print(f"{'Temp (°C)':<10} | {'Sales (Units)':<15} | {'Observation'}")
    print("-" * 45)

    # 1. Zip the data to see the pairs
    for temp, sales in zip(temp_data, sale_data):
        # 2. Logic: Create "Buckets" for the temperature
        if temp < 15:
            obs = "Cold Day"
        elif temp > 28:
            obs = "Heatwave"
        else:
            obs = "Mild"
        
        print(f"{temp:<10}°C | {sales:<15} | {obs}")

    # 3. Calculate Simple Correlation Logic
    # We compare the start of the week to the end
    temp_change = temp_data[-1] - temp_data[0]
    sale_change = sale_data[-1] - sale_data[0]

    print("-" * 45)
    print(f"Temperature Trend: {temp_change:+}°C")
    print(f"Sales Trend:       {sale_change:+} units")

    # 4. Insight: Determine the Relationship
    if (temp_change > 0 and sale_change < 0) or (temp_change < 0 and sale_change > 0):
        relationship = "Inverse (Negative) Correlation"
        note = "As it gets hotter, people buy LESS hot coffee."
    else:
        relationship = "Positive Correlation"
        note = "Sales move in the same direction as temperature."

    print(f"\n[INSIGHT]: {relationship}")
    print(f"Strategy: {note}")

analyze_weather_impact()
