# Library Management System

This Library Management System is a command-line application built using Python. It allows a librarian to either add or remove a book from the library and allows a reader to search a book by a title or author, borrow and return a book.

## Features

- **User Authentication**:
    - User registration and login system
    - Role-based access (Librarian/Reader)
    - Session management

- **Librarian Functions**:
    - Add new books to the library with input validation
    - Remove books from the library
    - View all books with borrower information

- **Reader Functions**:
    - Enhanced search with fuzzy matching by title or author
    - Borrow and return books with user tracking
    - View all books in the library
    - View personal borrowed books list
    - Continue browsing after actions

- **Enhanced Features**:
    - Input validation for all user inputs
    - Fuzzy search functionality for better user experience
    - User tracking for borrowed books
    - Improved error handling and user feedback
    - Enhanced user interface with better navigation

- **Design Principles**:
    - Object-Oriented Programming
    - Modular code organization
    - Proper error handling with custom exceptions
    - Input validation and data quality assurance
    - Comprehensive unit testing
    - PEP 8 style guidelines compliance

## Prerequisites
- Python 3.12 or higher

## How to Run
1. Clone the repository or download the project files to your local machine.
2. Ensure that Python is installed and accessible via the command line.
3. Open a terminal and navigate to the project directory.
4. Run the following command: "python -m interface.main"
5. Admin password: admin (hardcoded for librarian access)
6. New users can register through the Reader Access option
7. Follow the on-screen prompts to interact with the Library Management System.

## File Descriptions

### Core Models
- **book.py**: Manages individual book operations (borrow, return) with user tracking
- **author.py**: Handles author information and book associations
- **library.py**: Central library management with user authentication and book operations
- **user.py**: User account management and borrowed books tracking

### Interface
- **main.py**: Command-line interface with menu systems for librarians and readers

### Utilities
- **validation.py**: Input validation functions and fuzzy search implementation

### Data Files
- **library_data.json**: Persistent storage for book information
- **users_data.json**: Persistent storage for user accounts and borrowed books

## Testing
- Run the unit tests using the following command:
  ```bash
  python -m unittest discover -s tests
  ```
- Individual test files can be run separately:
  ```bash
  python -m unittest tests.test_book
  python -m unittest tests.test_library
  python -m unittest tests.test_author
  ```

## Development Approach

### Single Responsibility Principle
Each class has a specific responsibility:
- **Book.py**: Handles book-specific operations (borrow, return, status)
- **Author.py**: Manages author information and book associations
- **Library.py**: Orchestrates the collection of books and user management
- **User.py**: Manages user authentication and borrowed books tracking
- **validation.py**: Provides input validation and search utilities

### Modularity
The code is organized into separate modules with clear responsibilities, making it easy to maintain and extend.

### Data Persistence
Book data and user information are stored in JSON files, allowing persistence between application runs.

### User Management
The system supports user registration and authentication for readers, with a single hardcoded admin account for librarians. It tracks which user borrowed which book.

### Enhanced Search
Fuzzy search allows partial matches, making it easier to find books even with incomplete titles or author names.

### Input Validation
All user inputs are validated to ensure data quality and prevent empty or invalid entries.

### Error Handling
Comprehensive error handling provides clear feedback and prevents system crashes.

## Usage Examples

### For Librarians
1. Login with admin password: `admin`
2. Add books
3. Remove books from the library
4. View all books with borrower information

### For Readers
1. Register a new account or login with existing credentials
2. Search books by title or author (supports partial matching)
3. Borrow available books
4. Return borrowed books
5. View personal borrowed books list

## Future Enhancements
- Due date tracking for borrowed books
- Book categories and genres
- Advanced search filters
- Book reservation system
- Reading history and recommendations
