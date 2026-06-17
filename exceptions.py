class ExpenseTrackerError(Exception):
    """Base class for exceptions in the Expense Tracker application."""
    pass

class UsernameNotFoundError(ExpenseTrackerError):
    """Exception raised when a username is not found in the system."""
    pass

class InvalidPasswordError(ExpenseTrackerError):
    """Exception raised when an invalid password is provided."""
    pass

class UserAlreadyExistsError(ExpenseTrackerError):
    """Exception raised when trying to create a user that already exists."""
    pass

class TransactionNotFoundError(ExpenseTrackerError):
    """Exception raised when a transaction is not found in the system."""
    pass

class InvalidTransactionTypeError(ExpenseTrackerError):
    """Exception raised when an invalid transaction type is provided."""
    pass

class UsernameTooShortError(ExpenseTrackerError):
    """Exception raised when a username is too short."""
    pass

class UsernameTooLongError(ExpenseTrackerError):
    """Exception raised when a username is too long."""
    pass

class UsernameContainsSpacesError(ExpenseTrackerError):
    """Exception raised when a username contains spaces."""
    pass

class AgeOutOfRangeError(ExpenseTrackerError):
    """Exception raised when an age is out of the valid range."""
    pass

class InsufficientBalanceError(ExpenseTrackerError):
    """Exception raised when user doesn't have enough balance."""
    pass

class UserNotFoundError(ExpenseTrackerError):
    """Exception raised when a user is not found in the system."""
    pass