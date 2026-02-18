import random

def main():
    target = random.randint(1, 100)
    attempts = 0
    
    print("Guess the number between 1 and 100")
    
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            
            if guess < target:
                print("Higher")
            elif guess > target:
                print("Lower")
            else:
                print(f"Correct! You found it in {attempts} tries")
                break
        except ValueError:
            print("Please enter a valid number")

if __name__ == "__main__":
    main()