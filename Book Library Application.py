class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append(Book(title, author))

    def show_books(self):
        if not self.books:
            print("Library is empty.")
            return
        
        for i, book in enumerate(self.books, 1):
            status = "Borrowed" if book.is_borrowed else "Available"
            print(f"{i}. {book.title} by {book.author} [{status}]")

    def borrow_book(self, index):
        if 0 <= index < len(self.books):
            if not self.books[index].is_borrowed:
                self.books[index].is_borrowed = True
                print(f"You borrowed: {self.books[index].title}")
            else:
                print("Book is already out.")
        else:
            print("Invalid selection.")

def main():
    my_library = Library()
    my_library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    my_library.add_book("1984", "George Orwell")

    while True:
        print("\n1. View Books\n2. Add Book\n3. Borrow Book\n4. Exit")
        choice = input("Select: ")

        if choice == "1":
            my_library.show_books()
        elif choice == "2":
            t = input("Title: ")
            a = input("Author: ")
            my_library.add_book(t, a)
        elif choice == "3":
            my_library.show_books()
            idx = int(input("Enter number to borrow: ")) - 1
            my_library.borrow_book(idx)
        elif choice == "4":
            break

if __name__ == "__main__":
    main()