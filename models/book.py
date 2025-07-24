# Class representing a book in the library system

class Book:
    def __init__(self, title, author, status, borrowed_by=None):
        self.title = title.strip()
        self.author = author.strip()
        self.status = status # True = available & False = Borrowed
        self.borrowed_by = borrowed_by

    # Method to borrow books
    def borrow(self, username=None):
        # Check if the book is available
        if self.status:
            self.status = False # set it to borrowed
            self.borrowed_by = username
            return f"The book {self.title} has been successfully borrowed."
        else:
            return f"The book {self.title} is currently borrowed."

    # Method to return a borrowed book
    def return_book(self):
        if not self.status:  # Checking if book is borrowed
            self.status = True
            self.borrowed_by = None
            return f"You have successfully returned the book {self.title}."
        else:
            return f"The book {self.title} was not borrowed."

    def __str__(self):
        return f"{self.title} by {self.author}"


