import unittest
from models.author import Author

#Tests for the Author class
class TestAuthor(unittest.TestCase):
    def test_add_book(self):
        author = Author("Test Author")
        author.addbook("Test Book")
        self.assertEqual(len(author.books), 1)
        self.assertEqual(author.books[0], "Test Book")

if __name__ == '__main__':
    unittest.main()
