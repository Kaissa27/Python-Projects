import sys

def calculate_performance(purchase_price, current_price, shares):
    invested = purchase_price * shares
    current_val = current_price * shares
    gain_loss = current_val - invested
    percent_change = (gain_loss / invested) * 100 if invested > 0 else 0
    return invested, current_val, gain_loss, percent_change

def view_portfolio(portfolio):
    if not portfolio:
        print("Portfolio is empty.")
        return

    print(f"\n{'Symbol':<8} | {'Shares':<8} | {'Invested':<10} | {'Value':<10} | {'G/L %'}")
    print("-" * 55)

    total_invested = 0
    total_value = 0

    for symbol, data in portfolio.items():
        inv, val, gl, pc = calculate_performance(data['buy_price'], data['current_price'], data['shares'])
        total_invested += inv
        total_value += val
        print(f"{symbol:<8} | {data['shares']:<8} | {inv:<10.2f} | {val:<10.2f} | {pc:>+.2f}%")

    print("-" * 55)
    print(f"Total Portfolio Value: {total_value:.2f}")
    print(f"Total Profit/Loss: {total_value - total_invested:.2f}")

def main():
    portfolio = {
        "AAPL": {"shares": 10, "buy_price": 150.00, "current_price": 185.50},
        "TSLA": {"shares": 5, "buy_price": 250.00, "current_price": 240.20},
        "GOOG": {"shares": 8, "buy_price": 100.00, "current_price": 140.10}
    }

    while True:
        print("\nStock Tracker Menu")
        print("1. View Portfolio")
        print("2. Update Current Price")
        print("3. Exit")
        
        choice = input("Select: ")
        
        if choice == "1":
            view_portfolio(portfolio)
        elif choice == "2":
            sym = input("Enter Symbol: ").upper()
            if sym in portfolio:
                try:
                    portfolio[sym]["current_price"] = float(input("New Price: "))
                except ValueError:
                    print("Invalid price.")
            else:
                print("Symbol not found.")
        elif choice == "3":
            sys.exit()

if __name__ == "__main__":
    main()