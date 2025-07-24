# Class representing an author in the library system

class Author:
    def __init__(self, full_name):
        self.full_name = full_name
        self.books = []

    # method to add new books for each author
    def addbook(self, book_title):
        self.books.append(book_title)

    def __str__(self):
        return f"Author: {self.full_name}"


