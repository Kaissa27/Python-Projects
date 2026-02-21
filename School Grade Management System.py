import sys

def calculate_gpa(grades):
    if not grades:
        return 0.0
    return sum(grades.values()) / len(grades)

def get_grade_letter(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"

def main():
    students = {
        "S101": {"name": "Alice", "grades": {"Math": 95, "Science": 88, "History": 92}},
        "S102": {"name": "Bob", "grades": {"Math": 72, "Science": 75, "History": 80}},
    }

    while True:
        print("\nStudent Grade Portal")
        print("1. View Student Report")
        print("2. Add/Update Grade")
        print("3. Register New Student")
        print("4. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            sid = input("Enter Student ID: ").upper()
            if sid in students:
                data = students[sid]
                avg = calculate_gpa(data["grades"])
                print(f"\nReport for: {data['name']}")
                for sub, score in data["grades"].items():
                    print(f"{sub}: {score} ({get_grade_letter(score)})")
                print(f"Average Score: {avg:.2f} | Final Grade: {get_grade_letter(avg)}")
            else:
                print("Student not found.")

        elif choice == "2":
            sid = input("Enter Student ID: ").upper()
            if sid in students:
                subject = input("Enter Subject: ").capitalize()
                try:
                    score = int(input("Enter Score (0-100): "))
                    students[sid]["grades"][subject] = score
                    print("Grade updated.")
                except ValueError:
                    print("Invalid score.")
            else:
                print("Student not found.")

        elif choice == "3":
            sid = input("New ID: ").upper()
            name = input("Name: ").title()
            students[sid] = {"name": name, "grades": {}}
            print(f"Student {name} registered.")

        elif choice == "4":
            sys.exit()

if __name__ == "__main__":
    main()