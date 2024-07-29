class CustomError(Exception): # This is the base class for other exceptions.
    pass

class ValidationError(CustomError):
    # This class will be raised when there is a validation error.
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        