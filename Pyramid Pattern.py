def generate_pyramid():
    try:
        rows = int(input("Enter number of rows: "))
        char = input("Enter a single character: ")[:1] or "*"
        
        if rows < 1:
            print("Number of rows must be positive.")
            return

        for i in range(1, rows + 1):
            spaces = " " * (rows - i)
            pattern = (char + " ") * i
            print(f"{spaces}{pattern.strip()}")
            
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    generate_pyramid()