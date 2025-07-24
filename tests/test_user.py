import unittest
from models.user import User

#Tests for the User class
class TestUser(unittest.TestCase):

    # testing user initialization
    def test_user_initialization(self):
        user = User("testuser", "password123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "password123")
        self.assertEqual(user.role, "reader")
        self.assertEqual(user.borrowed_books, [])

    # testing user initialization with librarian role
    def test_user_initialization_librarian(self):
        user = User("admin", "adminpass", "librarian")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.role, "librarian")

    # testing adding borrowed book
    def test_add_borrowed_book(self):
        user = User("testuser", "password123")
        user.add_borrowed_book("Test Book")
        self.assertIn("Test Book", user.borrowed_books)

    # testing adding duplicate borrowed book
    def test_add_duplicate_borrowed_book(self):
        user = User("testuser", "password123")
        user.add_borrowed_book("Test Book")
        user.add_borrowed_book("Test Book")  # Should not add duplicate
        self.assertEqual(len(user.borrowed_books), 1)

    # testing removing borrowed book
    def test_remove_borrowed_book(self):
        user = User("testuser", "password123")
        user.add_borrowed_book("Test Book")
        user.remove_borrowed_book("Test Book")
        self.assertNotIn("Test Book", user.borrowed_books)

    # testing removing non-existent borrowed book
    def test_remove_nonexistent_borrowed_book(self):
        user = User("testuser", "password123")
        user.remove_borrowed_book("Non-existent Book")  # Should not cause error
        self.assertEqual(len(user.borrowed_books), 0)

    # testing string representation
    def test_str_representation(self):
        user = User("testuser", "password123")
        self.assertEqual(str(user), "User: testuser (reader)")

if __name__ == '__main__':
    unittest.main()