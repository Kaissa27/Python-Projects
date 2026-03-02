from abc import ABC, abstractmethod

# 1. Abstract Base Class
class Employee(ABC):
    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number

    # This forces every sub-class to have its own salary logic
    @abstractmethod
    def calculate_pay(self):
        pass

    def __str__(self):
        return f"ID: {self.id_number} | Name: {self.name}"

# 2. Inheritance: Full-Time Employee
class FullTimeEmployee(Employee):
    def __init__(self, name, id_number, monthly_salary):
        super().__init__(name, id_number)
        self.monthly_salary = monthly_salary

    def calculate_pay(self):
        return self.monthly_salary

# 3. Inheritance: Hourly Employee 
class HourlyEmployee(Employee):
    def __init__(self, name, id_number, hours_worked, hourly_rate):
        super().__init__(name, id_number)
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_pay(self):
        return self.hours_worked * self.hourly_rate

# 4. Manager Class (Managing other objects)
class Department:
    def __init__(self, dept_name):
        self.dept_name = dept_name
        self.staff = []

    def add_employee(self, emp):
        if isinstance(emp, Employee):
            self.staff.append(emp)
        else:
            print("Error: Only Employee objects can be added.")

    def run_payroll(self):
        print(f"--- Payroll for {self.dept_name} ---")
        total_payout = 0
        for emp in self.staff:
            pay = emp.calculate_pay()
            total_payout += pay
            print(f"{emp} | Payout: ${pay:,.2f}")
        print(f"Total Department Cost: ${total_payout:,.2f}\n")

def main():
    # Creating instances of different employee types
    dev = FullTimeEmployee("Alice Smith", "FT-101", 8500)
    intern = HourlyEmployee("Bob Jones", "HR-505", 120, 25)
    lead = FullTimeEmployee("Charlie Davis", "FT-102", 10500)

    # Creating the department and adding staff
    it_dept = Department("Information Technology")
    it_dept.add_employee(dev)
    it_dept.add_employee(intern)
    it_dept.add_employee(lead)

    # Executing the polymorphic payroll method
    it_dept.run_payroll()

if __name__ == "__main__":

    main()
