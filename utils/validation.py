# Input validation utilities

# Validate the book title and author
def validate_book_input(title, author):

    if not title or not title.strip():
        return False, "Book title cannot be empty"
    if not author or not author.strip():
        return False, "Author name cannot be empty"
    if len(title.strip()) < 2:
        return False, "Book title must be at least 2 characters"
    if len(author.strip()) < 2:
        return False, "Author name must be at least 2 characters"
    return True, "Valid"

# Validation for username and password
def validate_user_input(username, password):

    if not username or not username.strip():
        return False, "Username cannot be empty"
    if not password or len(password) < 3:
        return False, "Password must be at least 3 characters"
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters"
    return True, "Valid"

def fuzzy_search(query, text):

    query_words = query.lower().strip().split()
    text_lower = text.lower()
    return all(word in text_lower for word in query_words)