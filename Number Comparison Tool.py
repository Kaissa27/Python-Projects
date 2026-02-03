
# Number Comparison Tool
number = 4

if number > 5:
  print("The number is greater than 5.")
elif number == 5:
  print("The number is equal to 5.")
elif number == 4:
  print("The number is equal to 4.")
else:
  print("The number is less than 5.")

a = 2
b = 20

if a > 5 or b < 15:
  print("Either one of them is true")
else:
  print("Both conditions are false.")

# Number Comparison Tool

# Step 1: Get user input for two numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Step 2: Compare the numbers
print("\n--- Comparison Results ----")

if num1 == num2:
    print(f"Both numbers are equal: {num1}")
elif num1 > num2:
    print(f"{num1} is greater than {num2}")
else:
    print(f"{num2} is greater than {num1}")

# Step 3: Check if any number is zero
if num1 == 0 or num2 == 0:
    print("\nAt least one number is zero.")
else:
    print("\nBoth numbers are non-zero.")