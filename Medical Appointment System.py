import sys

def view_schedule(appointments):
    print(f"\n{'Doctor':<12} | {'Time Slot':<10} | {'Patient Name'}")
    print("-" * 40)
    for doc, slots in appointments.items():
        for time, patient in slots.items():
            status = patient if patient else "OPEN"
            print(f"{doc:<12} | {time:<10} | {status}")

def book_appointment(appointments):
    doc = input("Enter Doctor Name: ").title()
    if doc not in appointments:
        print("Doctor not found.")
        return

    time = input("Enter Slot (e.g., 09:00, 10:00): ")
    if time not in appointments[doc]:
        print("Invalid time slot.")
        return

    if appointments[doc][time] is not None:
        print(f"Error: {time} is already booked by {appointments[doc][time]}.")
    else:
        patient = input("Enter Patient Name: ").title()
        appointments[doc][time] = patient
        print(f"Success: Appointment confirmed for {patient} with Dr. {doc}.")

def main():
    # Nested dictionary representing Doctor -> Time Slot -> Patient
    appointments = {
        "Dr. Smith": {"09:00": None, "10:00": None, "11:00": None},
        "Dr. Jones": {"09:00": "Alice Brown", "10:00": None, "11:00": None}
    }

    while True:
        print("\nClinic Management System")
        print("1. View Full Schedule")
        print("2. Book Appointment")
        print("3. Cancel Appointment")
        print("4. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            view_schedule(appointments)
        elif choice == "2":
            book_appointment(appointments)
        elif choice == "3":
            doc = input("Doctor: ").title()
            time = input("Time Slot: ")
            if doc in appointments and time in appointments[doc]:
                appointments[doc][time] = None
                print("Appointment cancelled.")
        elif choice == "4":
            sys.exit()

if __name__ == "__main__":
    main()