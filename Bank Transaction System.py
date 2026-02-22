import sys

def process_transaction(accounts, acc_id, amount, t_type):
    if t_type == "Withdraw" and accounts[acc_id]["balance"] < amount:
        print("Insufficient funds.")
        return False
    
    if t_type == "Withdraw":
        accounts[acc_id]["balance"] -= amount
    else:
        accounts[acc_id]["balance"] += amount
        
    accounts[acc_id]["history"].append(f"{t_type}: ${amount:.2f}")
    return True

def main():
    accounts = {
        "A101": {"name": "Alice", "balance": 500.0, "history": []},
        "B202": {"name": "Bob", "balance": 1200.0, "history": []}
    }

    while True:
        print("\nATM Simulation")
        print("1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transaction History\n5. Exit")
        choice = input("Select: ")

        if choice == "5":
            sys.exit()

        acc_id = input("Enter Account ID: ").upper()
        if acc_id not in accounts:
            print("Account not found.")
            continue

        if choice == "1":
            print(f"Name: {accounts[acc_id]['name']} | Balance: ${accounts[acc_id]['balance']:.2f}")
        
        elif choice in ["2", "3"]:
            try:
                amt = float(input("Enter amount: "))
                t_type = "Deposit" if choice == "2" else "Withdraw"
                if process_transaction(accounts, acc_id, amt, t_type):
                    print(f"{t_type} successful.")
            except ValueError:
                print("Invalid amount.")

        elif choice == "4":
            print(f"\nStatement for {accounts[acc_id]['name']}:")
            for entry in accounts[acc_id]["history"]:
                print(f"- {entry}")
            print(f"Final Balance: ${accounts[acc_id]['balance']:.2f}")

if __name__ == "__main__":
    main()