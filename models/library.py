import json
import os
from models.book import Book
from models.user import User
from utils.validation import validate_book_input, validate_user_input, fuzzy_search

class Library:
    def __init__(self, file_path, users_file_path):
        self.books = []
        self.users = {}
        self.file_path = file_path
        self.users_file_path = users_file_path
        self.current_user = None
        self.load_books()
        self.load_users()

    # Method to load books from JSON file
    def load_books(self):
        try:
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0: # Check if the file exists and if it is not empty
                with open(self.file_path, "r") as file:
                    books_data = json.load(file)
                    for book_data in books_data:
                        title = book_data.get("title", "")
                        author = book_data.get("author", "")
                        status = book_data.get("status")
                        borrowed_by = book_data.get("borrowed_by")
                        if title.strip() and author.strip():  # Only load valid books
                            self.books.append(Book(title, author, status, borrowed_by))
            else:
                with open(self.file_path, "w") as file: # Create empty JSON file with an empty array (fix error with loading empty JSON file)
                    file.write("[]")
        except (json.JSONDecodeError, FileNotFoundError):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True) # If file is corrupted or doesn't exist a new one is created
            with open(self.file_path, "w") as file:
                file.write("[]")

    # Method to add (save) books to the JSON file
    def add_book_to_file(self):
        try:
            books_data = []
            for book in self.books:
                books_data.append({
                    "title": book.title,
                    "author": book.author,
                    "status": book.status,
                    "borrowed_by": book.borrowed_by
                })
            json_str = json.dumps(books_data, indent=4) # Convert to JSON string then you write to file
            with open(self.file_path, "w") as file:
                file.write(json_str)
        except Exception as e:
            print(f"Error saving books to file - {e}")

    # Method to add books in library
    def add_book(self, title, author):
        # Validate input
        is_valid, message = validate_book_input(title, author)
        if not is_valid:
            return f"Error: {message}"
        
        title = title.strip()
        author = author.strip()
        
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower(): # check if the book already exists
                return f"{title} by {author} is already in this library."
        try:
            new_book = Book(title, author, status=True)
            self.books.append(new_book)
            self.add_book_to_file() # add new book to the text file
            return f"{title} by {author} has been successfully added to the Library."
        except ValueError as e:
            return f"Error adding book to the library: {e}"

    # method to remove books from library
    def remove_book(self,title):
        for book in self.books:
            if book.title.lower() == title.lower(): # change to lower case in to match better
                self.books.remove(book)
                self.add_book_to_file() # remove book from text file
                return f"{title} has been successfully removed from the Library."

        return "Book not found in the Library."

    # method to search by title with fuzzy search
    def search_by_title(self, title):
        title = title.strip()
        # Exact match first
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        # Fuzzy search if no exact match
        for book in self.books:
            if fuzzy_search(title, book.title):
                return book
        return None

    # method to search by author with fuzzy search
    def search_by_author(self, author):
        author = author.strip()
        book_list = []
        # Exact match first
        for book in self.books:
            if book.author.lower() == author.lower():
                book_list.append(book)
        
        # Fuzzy search if no exact matches
        if not book_list:
            for book in self.books:
                if fuzzy_search(author, book.author):
                    book_list.append(book)

        if not book_list:
            return "There are no books by this author in this library."

        return book_list


    # method to borrow book
    def borrow_book(self, title):
        if not self.current_user:
            return "Please login to borrow books."
        
        book = self.search_by_title(title)
        if book is None:
            return "Book not found in the library."
        elif book.status:
            message = book.borrow(self.current_user.username)
            self.current_user.add_borrowed_book(title)
            self.add_book_to_file()
            self.save_users()
            return message
        elif not book.status:
            return f"{title} is currently borrowed by {book.borrowed_by}"


    # method to return a book
    def return_book(self, title):
        if not self.current_user:
            return "Please login to return books."
            
        book = self.search_by_title(title)
        if book is None:
            return f"The book {title} was not found."
        elif not book.status and book.borrowed_by == self.current_user.username:
            message = book.return_book()
            self.current_user.remove_borrowed_book(title)
            self.add_book_to_file()
            self.save_users()
            return message
        elif not book.status and book.borrowed_by != self.current_user.username:
            return f"You cannot return {title} as it was borrowed by {book.borrowed_by}."
        else:
            return f"The book {title} was not borrowed."

    # method to display all books in library
    def display_books(self):
        if self.books:
            book_list = []
            for idx, book in enumerate(self.books, 1):
                if book.status:
                    status_text = "Available"
                else:
                    status_text = f"Borrowed by {book.borrowed_by}"
                book_list.append(f"{idx}. {book.title} by {book.author} - {status_text}")
            return "\n".join(book_list)
        else:
            return "There are no books in this library."
    
    # User management methods
    def load_users(self):
        try:
            if os.path.exists(self.users_file_path) and os.path.getsize(self.users_file_path) > 0:
                with open(self.users_file_path, "r") as file:
                    users_data = json.load(file)
                    for username, user_data in users_data.items():
                        user = User(username, user_data["password"], user_data["role"])
                        user.borrowed_books = user_data.get("borrowed_books", [])
                        self.users[username] = user
            else:
                with open(self.users_file_path, "w") as file:
                    file.write("{}")
        except (json.JSONDecodeError, FileNotFoundError):
            os.makedirs(os.path.dirname(self.users_file_path), exist_ok=True)
            with open(self.users_file_path, "w") as file:
                file.write("{}")
    
    def save_users(self):
        try:
            users_data = {}
            for username, user in self.users.items():
                users_data[username] = {
                    "password": user.password,
                    "role": user.role,
                    "borrowed_books": user.borrowed_books
                }
            with open(self.users_file_path, "w") as file:
                json.dump(users_data, file, indent=4)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    
    def register_user(self, username, password):
        is_valid, message = validate_user_input(username, password)
        if not is_valid:
            return False, message
        
        username = username.strip()
        if username in self.users or username.lower() == "admin":
            return False, "Username already exists or is reserved"
        
        self.users[username] = User(username, password, "reader")
        self.save_users()
        return True, "User registered successfully"
    
    def login(self, username, password):
        username = username.strip()
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            return True, f"Welcome {username}!"
        return False, "Invalid username or password"
    
    def logout(self):
        if self.current_user:
            username = self.current_user.username
            self.current_user = None
            return f"Goodbye {username}!"
        return "No user logged in"