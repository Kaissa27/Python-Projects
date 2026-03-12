import datetime

# Custom Exception for better error handling
class OverdraftError(Exception):
    pass

class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        # Encapsulation: __balance is private to prevent direct tampering
        self.__balance = initial_balance
        self.transaction_history = []
        self._add_transaction("Account Created", initial_balance)

    def _add_transaction(self, note, amount):
        """Internal method to log activities."""
        entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": note,
            "amount": amount,
            "current_balance": self.__balance
        }
        self.transaction_history.append(entry)

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self._add_transaction("Deposit", amount)
            print(f"[+] ${amount:.2f} deposited. New Balance: ${self.__balance:.2f}")
        else:
            print("[!] Deposit amount must be positive.")

    def withdraw(self, amount):
        try:
            if amount > self.__balance:
                raise OverdraftError(f"Insufficient funds for withdrawal of ${amount}")
            
            if amount <= 0:
                print("[!] Withdrawal must be positive.")
                return

            self.__balance -= amount
            self._add_transaction("Withdrawal", -amount)
            print(f"[-] ${amount:.2f} withdrawn. Remaining: ${self.__balance:.2f}")
            
        except OverdraftError as e:
            print(f"[ERROR] {e}")

    def get_balance(self):
        """Getter method to safely view the private balance."""
        return self.__balance

    def display_statement(self):
        print(f"\n--- Statement for {self.account_holder} ---")
        print(f"{'Date':<18} | {'Activity':<15} | {'Amount':<10} | {'Balance'}")
        print("-" * 60)
        for t in self.transaction_history:
            print(f"{t['date']:<18} | {t['note']:<15} | {t['amount']:>10.2f} | ${t['current_balance']:>8.2f}")
        print("-" * 60)

def main():
    # Initialize account
    my_account = BankAccount("Satoshi Nakamoto", 1000)

    # Perform actions
    my_account.deposit(500)
    my_account.withdraw(200)
    my_account.withdraw(2000)  # This will trigger our OverdraftError
    my_account.deposit(150)

    # Show final statement
    my_account.display_statement()

if __name__ == "__main__":
    main()