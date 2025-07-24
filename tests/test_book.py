import unittest
from models.book import Book

#Tests for the Book class
class TestBook(unittest.TestCase):

    # testing that a book is initialized correctly
    def test_book_initialization(self):
        book = Book("Test Title", "Test Author", True)
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertTrue(book.status)
        self.assertIsNone(book.borrowed_by)
    
    # testing book initialization with borrowed_by parameter
    def test_book_initialization_with_borrower(self):
        book = Book("Test Title", "Test Author", False, "testuser")
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertFalse(book.status)
        self.assertEqual(book.borrowed_by, "testuser")

    # testing borrowing a book that is available (status = true)
    def test_book_borrow(self):
        book = Book("Test Title", "Test Author", True)
        message = book.borrow("testuser")
        self.assertFalse(book.status)
        self.assertEqual(book.borrowed_by, "testuser")
        self.assertEqual(message, "The book Test Title has been successfully borrowed.")

    # testing borrowing a book that is unavailable/borrowed (status = false)
    def test_borrow_unavailable_book(self):
        book = Book("Test Title", "Test Author", False, "otheruser")
        message = book.borrow("testuser")
        self.assertFalse(book.status)  # Status should remain False
        self.assertEqual(book.borrowed_by, "otheruser")  # Should remain with original borrower
        self.assertEqual(message, "The book Test Title is currently borrowed.")

    # testing returning a book that is borrowed
    def test_return_book(self):
        book = Book("Test Title", "Test Author", False, "testuser")
        message = book.return_book()
        self.assertTrue(book.status)
        self.assertIsNone(book.borrowed_by)
        self.assertEqual(message, "You have successfully returned the book Test Title.")

    # testing returning a book that was not borrowed
    def test_return_available_book(self):
        book = Book("Test Title", "Test Author", True)
        message = book.return_book()
        self.assertTrue(book.status)  # Status should remain True
        self.assertEqual(message, "The book Test Title was not borrowed.")

if __name__ == '__main__':
    unittest.main()