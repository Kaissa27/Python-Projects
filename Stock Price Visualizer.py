import matplotlib.pyplot as plt

def plot_stocks(stock_name, prices):
    days = list(range(1, len(prices) + 1))
    
    plt.plot(days, prices, marker='o', linestyle='-', color='b')
    plt.title(f"Price Trend for {stock_name}")
    plt.xlabel("Day")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.show()

# Sample data: 7 days of stock prices
prices_list = [150, 155, 153, 158, 162, 160, 165]
plot_stocks("TechCorp", prices_list)
