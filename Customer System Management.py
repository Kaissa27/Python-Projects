import sys

def add_customer(crm):
    cust_id = input("Enter Customer ID: ").strip().upper()
    if cust_id in crm:
        print("Error: ID already exists.")
        return
        
    name = input("Enter Name: ").strip().title()
    email = input("Enter Email: ").strip()
    try:
        spend = float(input("Enter Initial Total Spend: "))
        crm[cust_id] = {
            "name": name, 
            "email": email, 
            "spend": spend, 
            "status": "Active"
        }
        print(f"Customer {name} registered.")
    except ValueError:
        print("Invalid spend amount.")

def update_status(crm):
    cust_id = input("Enter Customer ID: ").strip().upper()
    if cust_id in crm:
        new_status = input("Enter new status (Active/Inactive): ").strip().capitalize()
        crm[cust_id]["status"] = new_status
        print("Status updated.")
    else:
        print("Customer not found.")

def view_all(crm):
    if not crm:
        print("No customers in system.")
        return

    print(f"\n{'ID':<8} | {'Name':<15} | {'Email':<20} | {'Spend':<10} | {'Status'}")
    print("-" * 65)
    
    for cid, data in crm.items():
        print(f"{cid:<8} | {data['name']:<15} | {data['email']:<20} | {data['spend']:<10.2f} | {data['status']}")

def main():
    crm_data = {}
    
    while True:
        print("\nCRM Dashboard")
        print("1. Register Customer")
        print("2. Update Customer Status")
        print("3. View All Customers")
        print("4. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            add_customer(crm_data)
        elif choice == "2":
            update_status(crm_data)
        elif choice == "3":
            view_all(crm_data)
        elif choice == "4":
            sys.exit()
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()