import hashlib

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed

def register_user(username: str, password: str, name: str, age: int):
    """Register a new user."""
    from database import get_user_by_username, save_user
    from models import User
    from exceptions import UserAlreadyExistsError, UsernameTooShortError, UsernameTooLongError, UsernameContainsSpacesError, AgeOutOfRangeError
    # check if user exists
    if get_user_by_username(username):
        raise UserAlreadyExistsError(f"User with username '{username}' already exists.")
    
    # Validate username
    if len(username) < 3:
        raise UsernameTooShortError("Username must be at least 3 characters long.")
    if len(username) > 20:
        raise UsernameTooLongError("Username must be at most 20 characters long.")
    if " " in username:
        raise UsernameContainsSpacesError("Username cannot contain spaces.")

    # Validate age
    if age < 0 or age > 150:
        raise AgeOutOfRangeError("Age must be between 0 and 150.")

    # Check if user already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        raise UserAlreadyExistsError(f"User with username '{username}' already exists.")

    # Hash the password
    hashed_password = hash_password(password)

    # Create a new user instance
    new_user = User(username=username, password=hashed_password, name=name, age=age)

    # Save the user to the database
    save_user(new_user)

def login_user(username: str, password: str):
    """Login a user."""
    from database import get_user_by_username
    from exceptions import UsernameNotFoundError, InvalidPasswordError

    user = get_user_by_username(username)
    if not user:
        raise UsernameNotFoundError(f"User with username '{username}' not found.")

    if not verify_password(password, user['password']):
        raise InvalidPasswordError("Invalid password.")

    return user