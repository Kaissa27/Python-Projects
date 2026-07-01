import random 

def rps_game():
    options = ["rock", "paper", "scissors"]
    user_score = 0
    cpu_score = 0

    print("--- Rock, Paper, Scissors (First to 3) ---")

    while user_score < 3 and cpu_score < 3:
        cpu_choice = random.choice(options)
        user_choice = input("\nRock, Paper, or Scissors? ").lower()

        if user_choice not in options:
            print("Invalid choice!")
            continue

        print(f"Computer chose: {cpu_choice}")

        if user_choice == cpu_choice:
            print("It's a tie!")
        elif (user_choice == "rock" and cpu_choice == "scissors") or \
             (user_choice == "paper" and cpu_choice == "rock") or \
             (user_choice == "scissors" and cpu_choice == "paper"):
            print("You win this round!")
            user_score += 1
        else:
            print("Computer wins this round!")
            cpu_score += 1
        
        print(f"Score: You {user_score} - {cpu_score} CPU")

    print("\nFinal Result: " + ("YOU WON THE GAME!" if user_score == 3 else "CPU WON!"))

# rps_game()
