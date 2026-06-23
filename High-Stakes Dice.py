import random
import time

def dice_casino():
    wallet = 100
    print("--- WELCOME TO THE PYTHON CASINO 🎲 ---")
    print(f"You're starting with: ${wallet}")

    while wallet > 0:
        print(f"\nCurrent Balance: ${wallet}")
        
        # 1. Get the Bet
        try:
            bet = input("Place your bet (or 'q' to quit): ")
            if bet.lower() == 'q':
                break
            
            bet = int(bet)
            if bet > wallet:
                print("You don't have that much money!")
                continue
            if bet <= 0:
                print("Minimum bet is $1.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        # 2. The Roll
        print("Rolling...")
        time.sleep(1)
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        print(f"🎲 {die1} + {die2} = {total}")

        # 3. Win/Loss Logic
        if total == 7 or total == 11:
            print(f"LUCKY! You won ${bet}!")
            wallet += bet
        elif die1 == 1 and die2 == 1:
            print("SNAKE EYES! The casino took everything! 😱")
            wallet = 0
        elif total in [2, 3, 12]:
            print(f"CRAPS! You lost ${bet}.")
            wallet -= bet
        else:
            print("No winner, no loser. Keep your bet.")

    if wallet <= 0:
        print("\nYou're broke! Security is escorting you out.")
    else:
        print(f"\nYou're leaving with ${wallet}. See you next time!")

# dice_casino()
