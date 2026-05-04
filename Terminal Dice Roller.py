import random

def dice_roller():
    print("Welcome to the 3D Dice Roller (Terminal Edition)")
    
    while True:
        input("\nPress Enter to roll the dice (or type 'q' to quit)... ")
        
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        
        print(f"🎲 You rolled a {die1} and a {die2}!")
        print(f"Total: {die1 + die2}")
        
        if die1 == die2:
            print("DOUBLES! Roll again!")
        
        choice = input("Roll again? (y/n): ").lower()
        if choice == 'n' or choice == 'q':
            break

# dice_roller()
