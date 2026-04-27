def calculate_split():
    print("--- Pro Bill Splitter ---")
    try:
        total_bill = float(input("Enter total bill amount: "))
        tip_percentage = float(input("Enter tip percentage (e.g. 15): "))
        people = int(input("How many people are splitting? "))
        
        grand_total = total_bill * (1 + tip_percentage / 100)
        share = grand_total / people
        
        print(f"\nTotal including tip: ${grand_total:.2f}")
        print(f"Each person owes: ${share:.2f}")
        
    except ValueError:
        print("Invalid input! Please enter numbers only.")

# calculate_split()
