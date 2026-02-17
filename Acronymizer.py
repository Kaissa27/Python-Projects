user_input = input("Enter a phrase: ")
words = user_input.split()

# List of words to ignore (all lowercase for easy matching)
stop_words = ["of", "the", "and", "in", "to", "for", "a", "an"]

acronym = ""

for i in words:
    # Check if the word (in lowercase) is NOT in our skip list
    if i.lower() not in stop_words:
        acronym += i[0].upper()

print(f"Your Acronym: {acronym}")