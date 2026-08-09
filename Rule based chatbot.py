def chatbot():
    print("Bot: Hey! I’m your manga buddy. Type 'quit' to exit.")
    while True:
        user = input("You: ").lower()
        if "manga" in user:
            print("Bot: What manga are you reading rn?")
        elif "hello" in user:
            print("Bot: Hey there!")
        elif "quit" in user:
            print("Bot: Bye! Go read more manga.")
            break
        else:
            print("Bot: Tell me more about that.")

chatbot()