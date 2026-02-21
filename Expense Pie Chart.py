import matplotlib.pyplot as plt

def generate_chart(data):
    categories = list(data.keys())
    amounts = list(data.values())

    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Monthly Expense Distribution')
    plt.axis('equal')
    plt.savefig('expense_chart.png')
    print("Chart saved as expense_chart.png")

def main():
    expenses = {
        'Rent': 1200,
        'Food': 450,
        'Utilities': 200,
        'Entertainment': 150,
        'Transport': 100,
        'Other': 80
    }
    
    generate_chart(expenses)

if __name__ == "__main__":
    main()