import time

def start_game():
    inventory = []
    
    print("--- WELCOME TO THE HAUNTED MANSION ---")
    time.sleep(1)
    print("You wake up in a cold, dark hallway. There are two doors.")
    
    # First Choice
    choice1 = input("Do you go through the LEFT door or the RIGHT door? ").lower()

    if choice1 == "left":
        print("\nYou enter a dusty Library. A shiny GOLD KEY is sitting on a desk.")
        take_key = input("Do you take the key? (yes/no): ").lower()
        if take_key == "yes":
            inventory.append("Gold Key")
            print("You put the key in your pocket.")
        
        print("There is nothing else here. You go back to the hallway.")
        # Continue to the final choice
        final_door(inventory)

    elif choice1 == "right":
        print("\nYou enter the Kitchen. A ghost is eating a sandwich!")
        print("He looks at you and screams. You run back to the hallway in terror.")
        final_door(inventory)
    
    else:
        print("You tripped over your own feet and stayed in the hallway.")
        final_door(inventory)

def final_door(inventory):
    print("\nYou see a massive iron door at the end of the hall.")
    action = input("Do you try to OPEN it or KICK it? ").lower()

    if action == "open":
        if "Gold Key" in inventory:
            print("\nYou use the Gold Key. The door creaks open... YOU ARE FREE! 🎉")
        else:
            print("\nThe door is locked. You are trapped forever! 👻")
    else:
        print("\nYou kicked the door and broke your toe. The ghost caught you. Game Over.")

# Start the adventure
start_game()
