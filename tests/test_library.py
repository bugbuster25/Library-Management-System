import unittest
from models.library import Library
from models.user import User
import json
import os
from models.book import Book

#Tests for the Library class
class TestLibrary(unittest.TestCase):

    # creates a library instance and test files before each test
    def setUp(self):
        self.test_file_path = "test_library_data.json"
        self.test_users_path = "test_users_data.json"
        self.library = Library(self.test_file_path, self.test_users_path)
        self.library.books = []
        self.library.users = {}
        self.library.current_user = None
        self.library.add_book_to_file()
        self.library.save_users()

    # cleans up the JSON files used for testing after each test
    def tearDown(self):
        for file_path in [self.test_file_path, self.test_users_path]:
            if os.path.exists(file_path):
                os.remove(file_path)

    # testing adding a book to the library with validation
    def test_add_book(self):
        message = self.library.add_book("Test Title", "Test Author")
        self.assertEqual(message, "Test Title by Test Author has been successfully added to the Library.")
        self.assertEqual(len(self.library.books), 1)

    # testing adding invalid book (empty title)
    def test_add_book_invalid_title(self):
        message = self.library.add_book("", "Test Author")
        self.assertTrue(message.startswith("Error:"))
        self.assertEqual(len(self.library.books), 0)

    # testing adding invalid book (empty author)
    def test_add_book_invalid_author(self):
        message = self.library.add_book("Test Title", "")
        self.assertTrue(message.startswith("Error:"))
        self.assertEqual(len(self.library.books), 0)

    # testing adding a duplicate book
    def test_add_duplicate_book(self):
        self.library.add_book("Test Title", "Test Author")
        message = self.library.add_book("Test Title", "Test Author")
        self.assertEqual(message, "Test Title by Test Author is already in this library.")
        self.assertEqual(len(self.library.books), 1)

    # testing removing book from the library
    def test_remove_book(self):
        self.library.add_book("Test Title", "Test Author")
        message = self.library.remove_book("Test Title")
        self.assertEqual(message, "Test Title has been successfully removed from the Library.")
        self.assertEqual(len(self.library.books), 0)

    # testing removing a book that does not exist
    def test_remove_nonexistent_book(self):
        message = self.library.remove_book("Non-existent Book")
        self.assertEqual(message, "Book not found in the Library.")

    # testing fuzzy search by title
    def test_search_by_title_fuzzy(self):
        self.library.add_book("Harry Potter", "J.K. Rowling")
        book = self.library.search_by_title("Harry")
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "Harry Potter")

    # testing search by nonexistent title
    def test_search_by_nonexistent_title(self):
        book = self.library.search_by_title("Non-existent Title")
        self.assertIsNone(book)

    # testing fuzzy search by author
    def test_search_by_author_fuzzy(self):
        self.library.add_book("Test Title 1", "J.K. Rowling")
        self.library.add_book("Test Title 2", "J.K. Rowling")
        books = self.library.search_by_author("Rowling")
        self.assertEqual(len(books), 2)

    # testing user registration
    def test_register_user(self):
        success, message = self.library.register_user("testuser", "password123")
        self.assertTrue(success)
        self.assertEqual(message, "User registered successfully")
        self.assertIn("testuser", self.library.users)

    # testing user registration with invalid input
    def test_register_user_invalid(self):
        success, message = self.library.register_user("", "password123")
        self.assertFalse(success)
        self.assertTrue(message.startswith("Username cannot be empty"))

    # testing user registration with reserved username
    def test_register_user_reserved_username(self):
        success, message = self.library.register_user("admin", "password123")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists or is reserved")

    # testing user login
    def test_login_user(self):
        self.library.register_user("testuser", "password123")
        success, message = self.library.login("testuser", "password123")
        self.assertTrue(success)
        self.assertEqual(message, "Welcome testuser!")
        self.assertIsNotNone(self.library.current_user)

    # testing user login with wrong credentials
    def test_login_user_wrong_credentials(self):
        self.library.register_user("testuser", "password123")
        success, message = self.library.login("testuser", "wrongpassword")
        self.assertFalse(success)
        self.assertEqual(message, "Invalid username or password")

    # testing borrowing a book with user tracking
    def test_borrow_book_with_user(self):
        self.library.register_user("testuser", "password123")
        self.library.login("testuser", "password123")
        self.library.add_book("Test Book", "Test Author")
        
        message = self.library.borrow_book("Test Book")
        self.assertEqual(message, "The book Test Book has been successfully borrowed.")
        
        book = self.library.search_by_title("Test Book")
        self.assertFalse(book.status)
        self.assertEqual(book.borrowed_by, "testuser")
        self.assertIn("Test Book", self.library.current_user.borrowed_books)

    # testing borrowing without login
    def test_borrow_book_no_login(self):
        self.library.add_book("Test Book", "Test Author")
        message = self.library.borrow_book("Test Book")
        self.assertEqual(message, "Please login to borrow books.")

    # testing returning a book with user tracking
    def test_return_book_with_user(self):
        self.library.register_user("testuser", "password123")
        self.library.login("testuser", "password123")
        self.library.add_book("Test Book", "Test Author")
        self.library.borrow_book("Test Book")
        
        message = self.library.return_book("Test Book")
        self.assertEqual(message, "You have successfully returned the book Test Book.")
        
        book = self.library.search_by_title("Test Book")
        self.assertTrue(book.status)
        self.assertIsNone(book.borrowed_by)
        self.assertNotIn("Test Book", self.library.current_user.borrowed_books)

    # testing returning book borrowed by different user
    def test_return_book_different_user(self):
        # First user borrows book
        self.library.register_user("user1", "password123")
        self.library.login("user1", "password123")
        self.library.add_book("Test Book", "Test Author")
        self.library.borrow_book("Test Book")
        self.library.logout()
        
        # Second user tries to return it
        self.library.register_user("user2", "password123")
        self.library.login("user2", "password123")
        message = self.library.return_book("Test Book")
        self.assertEqual(message, "You cannot return Test Book as it was borrowed by user1.")

    # testing display books with borrower information
    def test_display_books_with_borrower(self):
        self.library.register_user("testuser", "password123")
        self.library.login("testuser", "password123")
        self.library.add_book("Test Title 1", "Test Author")
        self.library.add_book("Test Title 2", "Test Author")
        self.library.borrow_book("Test Title 1")
        
        message = self.library.display_books()
        self.assertIn("Test Title 1 by Test Author - Borrowed by testuser", message)
        self.assertIn("Test Title 2 by Test Author - Available", message)

    # testing logout
    def test_logout(self):
        self.library.register_user("testuser", "password123")
        self.library.login("testuser", "password123")
        message = self.library.logout()
        self.assertEqual(message, "Goodbye testuser!")
        self.assertIsNone(self.library.current_user)

if __name__ == '__main__':
    unittest.main()