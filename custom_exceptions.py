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

# The next few classes will be code for errors in 'def evaluate'
class EvaluationError(Exception):
    # This is the base class for errors that are evaluation-related.
    pass

class UnssupportedOperatorError(EvaluationError):
    # This is raised when an unsupported operator is encountered.
    def __init__(self, operator):
        super().__init__(f"Unsupported operator: '{operator}'")

class TypeError(EvaluationError):
    # Raised when types are incompatible for evaluation.
    def __init__(self, left, right):
        super().__init__(f"Invalid types: left operand type '{type(left).__name__}', right operand type '{type(right).__name__}'")
    
# The next few lines are based on most if not all the parse functions, or will contribute to them.
class ParseError(Exception):
    # Base class for parsing errors.
    pass

class ExpectedKeywordError(ParseError):
    def __init__(self, expected, found):
        super().__init__(f"Expected'{expected}, but found {found}'.")

class InvalidConditionError(ParseError):
    def __init__(self):
        super().__init__("Condition in 'if' statement cannot be empty or invalid.")