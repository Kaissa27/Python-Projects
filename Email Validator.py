import re

def is_valid_email(email):
    email = email.strip()
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.fullmatch(email_regex, email))

def main():
    user_input = input("Enter an email address: ")
    
    if is_valid_email(user_input):
        print(f"VALID: {user_input}")
    else:
        print(f"INVALID: {user_input}")

if __name__ == "__main__":
    main()