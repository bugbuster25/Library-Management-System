import unittest
from utils.validation import validate_book_input, validate_user_input, fuzzy_search

#Tests for the validation utilities
class TestValidation(unittest.TestCase):

    # testing valid book input
    def test_validate_book_input_valid(self):
        is_valid, message = validate_book_input("Test Title", "Test Author")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid")

    # testing empty book title
    def test_validate_book_input_empty_title(self):
        is_valid, message = validate_book_input("", "Test Author")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Book title cannot be empty")

    # testing empty book author
    def test_validate_book_input_empty_author(self):
        is_valid, message = validate_book_input("Test Title", "")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Author name cannot be empty")

    # testing short book title
    def test_validate_book_input_short_title(self):
        is_valid, message = validate_book_input("A", "Test Author")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Book title must be at least 2 characters")

    # testing short author name
    def test_validate_book_input_short_author(self):
        is_valid, message = validate_book_input("Test Title", "A")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Author name must be at least 2 characters")

    # testing valid user input
    def test_validate_user_input_valid(self):
        is_valid, message = validate_user_input("testuser", "password123")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid")

    # testing empty username
    def test_validate_user_input_empty_username(self):
        is_valid, message = validate_user_input("", "password123")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Username cannot be empty")

    # testing short password
    def test_validate_user_input_short_password(self):
        is_valid, message = validate_user_input("testuser", "12")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Password must be at least 3 characters")

    # testing short username
    def test_validate_user_input_short_username(self):
        is_valid, message = validate_user_input("ab", "password123")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Username must be at least 3 characters")

    # testing fuzzy search exact match
    def test_fuzzy_search_exact_match(self):
        result = fuzzy_search("Harry Potter", "Harry Potter and the Philosopher's Stone")
        self.assertTrue(result)

    # testing fuzzy search partial match
    def test_fuzzy_search_partial_match(self):
        result = fuzzy_search("Harry", "Harry Potter and the Philosopher's Stone")
        self.assertTrue(result)

    # testing fuzzy search multiple words
    def test_fuzzy_search_multiple_words(self):
        result = fuzzy_search("Harry Stone", "Harry Potter and the Philosopher's Stone")
        self.assertTrue(result)

    # testing fuzzy search no match
    def test_fuzzy_search_no_match(self):
        result = fuzzy_search("Twilight", "Harry Potter and the Philosopher's Stone")
        self.assertFalse(result)

    # testing fuzzy search case insensitive
    def test_fuzzy_search_case_insensitive(self):
        result = fuzzy_search("HARRY potter", "Harry Potter and the Philosopher's Stone")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()