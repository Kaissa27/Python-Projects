import sys

def calculate_pay(salary):
    tax_rate = 0.20
    tax_amount = salary * tax_rate
    net_pay = salary - tax_amount
    return tax_amount, net_pay

def add_employee(staff):
    emp_id = input("Enter Employee ID: ").strip().upper()
    if emp_id in staff:
        print("Error: ID already exists.")
        return
        
    name = input("Enter Name: ").strip().title()
    try:
        salary = float(input("Enter Monthly Gross Salary: "))
        tax, net = calculate_pay(salary)
        
        staff[emp_id] = {
            "name": name,
            "gross": salary,
            "tax": tax,
            "net": net
        }
        print(f"Record created for {name}.")
    except ValueError:
        print("Invalid salary amount.")

def view_payroll(staff):
    if not staff:
        print("No employee records found.")
        return

    print(f"\n{'ID':<8} | {'Name':<15} | {'Gross':<10} | {'Tax (20%)':<10} | {'Net Pay'}")
    print("-" * 60)
    
    for eid, data in staff.items():
        print(f"{eid:<8} | {data['name']:<15} | {data['gross']:<10.2f} | {data['tax']:<10.2f} | {data['net']:<10.2f}")

def main():
    staff_data = {}
    
    while True:
        print("\nPayroll Management")
        print("1. Add Employee")
        print("2. View Payroll Summary")
        print