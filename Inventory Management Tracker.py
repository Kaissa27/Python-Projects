import sys

def add_item(inventory):
    name = input("Enter item name: ").strip().lower()
    try:
        qty = int(input("Enter quantity: "))
        price = float(input("Enter price per unit: "))
        inventory[name] = {"quantity": qty, "price": price}
        print(f"Added {name} to inventory.")
    except ValueError:
        print("Invalid input. Use numbers for quantity and price.")

def update_stock(inventory):
    name = input("Enter item name to update: ").strip().lower()
    if name in inventory:
        try:
            new_qty = int(input(f"Enter new quantity for {name}: "))
            inventory[name]["quantity"] = new_qty
            print(f"Updated {name} stock.")
        except ValueError:
            print("Invalid quantity.")
    else:
        print("Item not found.")

def view_inventory(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    print(f"\n{'Item':<15} | {'Qty':<5} | {'Price':<10} | {'Status'}")
    print("-" * 45)
    
    for name, data in inventory.items():
        status = "LOW STOCK" if data["quantity"] < 5 else "OK"
        print(f"{name.capitalize():<15} | {data['quantity']:<5} | {data['price']:<10.2f} | {status}")

def main():
    inventory = {}
    
    while True:
        print("\nInventory Menu")
        print("1. Add/Overwrite Item")
        print("2. Update Quantity")
        print("3. View Inventory")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            add_item(inventory)
        elif choice == "2":
            update_stock(inventory)
        elif choice == "3":
            view_inventory(inventory)
        elif choice == "4":
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()