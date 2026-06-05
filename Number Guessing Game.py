import random

def guess_the_number():
    secret = random.randint(1, 100)
    lives = 7
    print("I'm thinking of a number between 1 and 100.")

    while lives > 0:
        print(f"\nYou have {lives} lives left.")
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("That's not a number! Try again.")
            continue

        if guess == secret:
            print(f" You win! The number was {secret}.")
            return
        elif guess < secret:
            print("Too low! ")
        else:
            print("Too high! ")
        
        lives -= 1

    print(f"\nGame Over! The number was {secret}. Better luck next time!")

# guess_the_number()
