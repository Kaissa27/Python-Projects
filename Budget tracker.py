import sys

def calculate_budget(total_budget, expenses):
    total_spent = sum(expenses.values())
    remaining = total_budget - total_spent
    return total_spent, remaining

def main():
    print("Budget Tracker")
    
    try:
        budget = float(input("Enter total budget: "))
    except ValueError:
        print("Invalid number.")
        sys.exit()

    expenses = {}
    
    while True:
        category = input("Enter category (or 'done' to finish): ").strip().lower()
        if category == 'done':
            break
            
        try:
            amount = float(input(f"Enter amount for {category}: "))
            expenses[category] = expenses.get(category, 0) + amount
        except ValueError:
            print("Invalid amount.")

    spent, left = calculate_budget(budget, expenses)

    print("\nSummary")
    for cat, amt in expenses.items():
        print(f"{cat.capitalize()}: {amt:.2f}")
    
    print("-" * 15)
    print(f"Total Spent: {spent:.2f}")
    print(f"Remaining: {left:.2f}")

    if left < 0:
        print("Status: Over Budget")
    else:
        print("Status: Under Budget")

if __name__ == "__main__":
    main()