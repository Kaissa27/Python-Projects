import sys

def calculate_fees(days, rate):
    base_price = days * rate
    tax = base_price * 0.15
    total = base_price + tax
    return base_price, tax, total

def show_fleet(fleet):
    print(f"\n{'ID':<5} | {'Vehicle':<15} | {'Type':<10} | {'Daily Rate':<10} | {'Status'}")
    print("-" * 60)
    for vid, details in fleet.items():
        status = "Available" if details["available"] else "Rented"
        print(f"{vid:<5} | {details['name']:<15} | {details['type']:<10} | {details['rate']:<10.2f} | {status}")

def main():
    fleet = {
        "V01": {"name": "Toyota Camry", "type": "Sedan", "rate": 50.00, "available": True},
        "V02": {"name": "Ford F-150", "type": "Truck", "rate": 80.00, "available": True},
        "V03": {"name": "Tesla Model 3", "type": "Electric", "rate": 100.00, "available": False},
        "V04": {"name": "Honda CR-V", "type": "SUV", "rate": 70.00, "available": True}
    }

    while True:
        print("\nRental Management Menu")
        print("1. View Fleet")
        print("2. Rent a Vehicle")
        print("3. Return a Vehicle")
        print("4. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            show_fleet(fleet)
        elif choice == "2":
            vid = input("Enter Vehicle ID: ").upper()
            if vid in fleet and fleet[vid]["available"]:
                try:
                    days = int(input("How many days? "))
                    base, tax, total = calculate_fees(days, fleet[vid]["rate"])
                    fleet[vid]["available"] = False
                    print(f"\nReceipt for {fleet[vid]['name']}:")
                    print(f"Base: {base:.2f} | Tax: {tax:.2f} | Total: {total:.2f}")
                except ValueError:
                    print("Invalid duration.")
            else:
                print("Vehicle not available or ID wrong.")
        elif choice == "3":
            vid = input("Enter ID to return: ").upper()
            if vid in fleet:
                fleet[vid]["available"] = True
                print(f"{fleet[vid]['name']} is now back in stock.")
        elif choice == "4":
            sys.exit()

if __name__ == "__main__":
    main()