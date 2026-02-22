import sys
from datetime import datetime

def calculate_stay(check_in, check_out, daily_rate):
    fmt = "%Y-%m-%d"
    d1 = datetime.strptime(check_in, fmt)
    d2 = datetime.strptime(check_out, fmt)
    days = (d2 - d1).days
    
    if days <= 0:
        return 0, 0
    
    total = days * daily_rate
    return days, total

def main():
    rooms = {
        "101": {"type": "Standard", "rate": 100, "guest": None},
        "102": {"type": "Deluxe", "rate": 180, "guest": None},
        "201": {"type": "Suite", "rate": 350, "guest": None}
    }

    while True:
        print("\nHotel Management System")
        print("1. View Room Status\n2. Book Room\n3. Check-out\n4. Exit")
        choice = input("Select: ")

        if choice == "1":
            print(f"\n{'Room':<6} | {'Type':<10} | {'Price':<8} | {'Status'}")
            for r_id, info in rooms.items():
                status = f"Occupied ({info['guest']})" if info['guest'] else "Available"
                print(f"{r_id:<6} | {info['type']:<10} | ${info['rate']:<8} | {status}")

        elif choice == "2":
            r_id = input("Enter Room ID: ")
            if r_id in rooms and rooms[r_id]["guest"] is None:
                rooms[r_id]["guest"] = input("Guest Name: ").title()
                print(f"Room {r_id} booked successfully.")
            else:
                print("Room unavailable or doesn't exist.")

        elif choice == "3":
            r_id = input("Enter Room ID for check-out: ")
            if r_id in rooms and rooms[r_id]["guest"]:
                print("Enter dates as YYYY-MM-DD")
                cin = input("Check-in: ")
                cout = input("Check-out: ")
                
                try:
                    days, total = calculate_stay(cin, cout, rooms[r_id]["rate"])
                    if days > 0:
                        print(f"\nGuest: {rooms[r_id]['guest']}")
                        print(f"Stay Duration: {days} nights")
                        print(f"Total Bill: ${total:.2f}")
                        rooms[r_id]["guest"] = None
                    else:
                        print("Invalid dates. Check-out must be after check-in.")
                except ValueError:
                    print("Date format error. Use YYYY-MM-DD.")
            else:
                print("Room is not occupied.")

        elif choice == "4":
            sys.exit()

if __name__ == "__main__":
    main()