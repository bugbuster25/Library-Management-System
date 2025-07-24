import os
import sys
from models.library import Library
from models.book import Book

# User authentication
def authenticate_user(library):
    while True:
        print("\n=== User Authentication ===")
        print("1. Login")
        print("2. Register New User")
        print("3. Back to Main Menu")
        
        try:
            choice = int(input("Choose option (1-3): "))
            
            if choice == 1:
                username = input("Username: ")
                password = input("Password: ")
                success, message = library.login(username, password)
                print(message)
                if success:
                    return True
            elif choice == 2:
                username = input("Choose username: ")
                password = input("Choose password: ")
                success, message = library.register_user(username, password)
                print(message)
            elif choice == 3:
                return False
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Librarian view
def librarian_menu(library):
    while True:
        print("\n=== Librarian Menu ===")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Display All Books")
        print("4. Back to Main Menu")
        print("5. Exit")

        try:
            choice = int(input("Choose option (1-5): "))

            match choice:
                case 1:  # Adding a new book
                    title = input("Enter book title: ")
                    author = input("Enter book author: ")
                    print(library.add_book(title, author))

                case 2:  # Removing a book
                    title = input("Enter book title: ")
                    print(library.remove_book(title))

                case 3:  # Displaying all books
                    print("These are the books in the Library: ")
                    print(library.display_books())

                case 4:  # Back to Main Menu
                    return

                case 5:  # Exiting
                    print("Goodbye! :)")
                    sys.exit(0)

                case _:  # Invalid choice
                    print("Invalid choice. Please enter a number between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a number.")

# Reader view
def reader_menu(library):
    while True:
        print(f"\n=== Reader Menu ===")
        print("1. Search for Book by Title")
        print("2. Search for Book by Author")
        print("3. Display All Books")
        print("4. Return a Book")
        print("5. View My Borrowed Books")
        print("6. Logout")
        print("7. Exit")

        try:
            choice = int(input("Choose option (1-7): "))

            match choice:
                case 1:  # Searching for a book by title
                    title = input("Enter the book title: ")
                    book = library.search_by_title(title)
                    if isinstance(book, Book):
                        status_text = "Available" if book.status else f"Borrowed by {book.borrowed_by}"
                        print(f"Found: {book.title} by {book.author} - {status_text}")
                        if book.status:
                            borrow_choice = input("Do you want to borrow this book? (y/n): ").lower()
                            if borrow_choice in ['y', 'yes']:
                                message = library.borrow_book(book.title)
                                print(message)
                    else:
                        print("Book not found in the library.")

                case 2:  # Searching for books by author
                    author = input("Enter the author's name: ")
                    books = library.search_by_author(author)
                    if isinstance(books, list) and books:
                        print(f"\nBooks by {author}:")
                        for idx, book in enumerate(books, 1):
                            status_text = "Available" if book.status else f"Borrowed by {book.borrowed_by}"
                            print(f"{idx}. {book.title} - {status_text}")
                        
                        borrow_choice = input("\nEnter book number to borrow (or press Enter to skip): ")
                        if borrow_choice.strip():
                            try:
                                book_idx = int(borrow_choice) - 1
                                if 0 <= book_idx < len(books):
                                    selected_book = books[book_idx]
                                    if selected_book.status:
                                        print(library.borrow_book(selected_book.title))
                                    else:
                                        print(f"The book {selected_book.title} is currently borrowed.")
                                else:
                                    print("Invalid book number.")
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                    else:
                        print(books if isinstance(books, str) else "No books found by this author.")

                case 3:  # Displaying all books in the library
                    print("\n=== All Books in Library ===")
                    print(library.display_books())
                    if library.books:
                        borrow_choice = input("\nEnter book number to borrow (or press Enter to skip): ")
                        if borrow_choice.strip():
                            try:
                                book_idx = int(borrow_choice) - 1
                                if 0 <= book_idx < len(library.books):
                                    book = library.books[book_idx]
                                    if book.status:
                                        print(library.borrow_book(book.title))
                                    else:
                                        print(f"{book.title} is currently borrowed.")
                                else:
                                    print("Invalid book number.")
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")

                case 4:  # Returning a book
                    title = input("Enter the book title you'd like to return: ")
                    print(library.return_book(title))

                case 5:  # View borrowed books
                    if library.current_user.borrowed_books:
                        print("\n=== Your Borrowed Books ===")
                        for idx, book_title in enumerate(library.current_user.borrowed_books, 1):
                            print(f"{idx}. {book_title}")
                    else:
                        print("You have no borrowed books.")

                case 6:  # Logout
                    print(library.logout())
                    return

                case 7:  # Exiting
                    print("Goodbye! :)")
                    sys.exit(0)

                case _:  # Invalid choice
                    print("Invalid choice. Please enter a number between 1 and 7.")

        except ValueError:
            print("Invalid input. Please enter a number.")

# Run the library management system
def main():
    try:
        # Use relative paths for better portability
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        library_file = os.path.join(base_path, "data", "library_data.json")
        users_file = os.path.join(base_path, "data", "users_data.json")
        
        library = Library(library_file, users_file)

        print("\n" + "="*50)
        print("    Welcome to the Library Management System!")
        print("="*50)

        while True:
            print("\n=== Main Menu ===")
            print("1. Librarian Login")
            print("2. Reader Access")
            print("3. Exit")

            try:
                choice = int(input("Choose option (1-3): "))

                if choice == 1:
                    password = input("Enter Admin Password: ")
                    if password == "admin":
                        librarian_menu(library)
                    else:
                        print("Invalid admin password.")

                elif choice == 2:
                    if authenticate_user(library):
                        reader_menu(library)

                elif choice == 3:
                    if library.current_user:
                        print(library.logout())
                    print("Thank you for using the Library Management System!")
                    sys.exit(0)

                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")

            except ValueError:
                print("Invalid input. Please enter a number.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()