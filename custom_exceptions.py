class CustomError(Exception): # This is the base class for other exceptions.
    pass

class ValidationError(CustomError):
    # This class will be raised when there is a validation error.
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotFoundError(CustomError):
    # This is raised when an item is not found.
    def __init__(self, item):
        self.message = f"{item} not found."
        super().__init__(self.message)

class VariableParseError(Exception):
    # This should be raised in parse_variable on parser.py when there is an error parsing a variable.
    def __init__(self, message, token=None):
        super().__init__(message)
        self.token = token # This line is an optional token reference for debugging purposes.