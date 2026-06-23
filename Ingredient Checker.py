# Ingredients Checker

# Step 1: Define the recipe ingredients
recipe_ingredients = {"flour", "sugar", "butter", "eggs", "milk"}

# Step 2: Get user input for available ingredients
user_input = input("Enter the ingredients you have (separated by commas): ")
user_ingredients = set(user_input.split(", "))

# Step 3: Compare Ingredients
missing_ingredients = recipe_ingredients - user_ingredients
extra_ingredients = user_ingredients - recipe_ingredients

# Step 4: Display Results
print("\n--- Ingredient Check Results ----")
if missing_ingredients:
    print(f"You are missing the following ingredients: {', '.join(missing_ingredients)}")
else:
    print("You have all the ingredients needed.")

if extra_ingredients:
    print(f"You have extra ingredients: {', '.join(extra_ingredients)}")
else:
    print("You have all the ingredients needed.")
