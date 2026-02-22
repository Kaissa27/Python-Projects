import sys

def calculate_total(order, menu):
    subtotal = 0
    for item, qty in order.items():
        subtotal += menu[item] * qty
    service_charge = subtotal * 0.10
    return subtotal, service_charge, subtotal + service_charge

def main():
    menu = {
        "Burger": 12.00,
        "Pizza": 15.50,
        "Pasta": 13.00,
        "Salad": 9.00,
        "Soda": 2.50
    }
    
    table_orders = {}

    while True:
        print("\nRestaurant POS System")
        print("1. View Menu\n2. Take Order\n3. Generate Bill\n4. Exit")
        choice = input("Select: ")

        if choice == "1":
            print(f"\n{'Item':<12} | {'Price'}")
            print("-" * 20)
            for item, price in menu.items():
                print(f"{item:<12} | ${price:.2f}")

        elif choice == "2":
            table = input("Enter Table Number: ")
            if table not in table_orders:
                table_orders[table] = {}
            
            while True:
                item = input("Enter item (or 'done'): ").title()
                if item == "Done": break
                if item in menu:
                    try:
                        qty = int(input(f"Quantity for {item}: "))
                        table_orders[table][item] = table_orders[table].get(item, 0) + qty
                    except ValueError:
                        print("Invalid quantity.")
                else:
                    print("Item not on menu.")

        elif choice == "3":
            table = input("Enter Table Number: ")
            if table in table_orders and table_orders[table]:
                sub, svc, total = calculate_total(table_orders[table], menu)
                print(f"\n--- Receipt: Table {table} ---")
                for item, qty in table_orders[table].items():
                    print(f"{item:<12} x{qty:<2} : ${menu[item]*qty:>6.2f}")
                print("-" * 25)
                print(f"Subtotal:       ${sub:>6.2f}")
                print(f"Service (10%):  ${svc:>6.2f}")
                print(f"Total:          ${total:>6.2f}")
                del table_orders[table]
            else:
                print("No active order for this table.")

        elif choice == "4":
            sys.exit()

if __name__ == "__main__":
    main()