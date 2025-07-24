# Class representing a user in the library system

class User:
    def __init__(self, username, password, role="reader"):
        self.username = username.strip()
        self.password = password
        self.role = role  # "reader" or "librarian"
        self.borrowed_books = []

    def add_borrowed_book(self, book_title):
        if book_title not in self.borrowed_books:
            self.borrowed_books.append(book_title)

    def remove_borrowed_book(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)

    def __str__(self):
        return f"User: {self.username} ({self.role})"