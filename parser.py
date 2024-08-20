from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    STRNG = 2
    IDENTIFIER = 3
    LPARREN = 4
    RPARREN = 5
    LBRACKET = 6
    RBRACKET = 7

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    
    def __repr__(self):
        if self.detailed:
            return f"Token of type {self.token_type} with value '{self.value}'"
        return f"Token({self.token_type}, {self.value})"
        
class SyntaxError(Exception):
    pass

class CustomSyntaxError(SyntaxError):
    def __init__(self, message, line=None, coluumn=None, token=None):
        super().__init__(message)
        self.line = line
        self.column = coluumn
        self.token = token

    def __str__(self):
        location = f"(Line: {self.line}, Column: {self.column})" if self.line is not None else ""
        if self.token:
            return f"{super().__str__()} Token: '{self.token}'{location}"
        return f"{super().__str__()}{location}"

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



class ASTNode:
    def __init__(self, token, *args):
        self.token = token
        self.children = args  # Store multiple child nodes or values in a list

    def __str__(self):
        return f"{self.token}({', '.join(str(child) for child in self.children)})"

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__("PROGRAM", *statements)


    
    def evaluate(self):
    # Type check
        if not isinstance(self.left, (int, float)) or not isinstance(self.right, (int, float)):
            raise TypeError(self.left, self.right)

        if self.operator == '+':
            return self.left + self.right
        elif self.operator == '-':
            return self.left - self.right
        elif self.operator == '*':
            return self.left * self.right
        elif self.operator == '/':
            if self.right == 0:
                raise ZeroDivisionError(f"Cannot divide {self.left} by zero.")
            return self.left / self.right
        elif self.operator == '**':
            return pow(self.left, self.right)
        else:
            raise UnsupportedOperatorError(self.operator)
    def __str__(self):
        return f"{self.left} {self.operator} {self.right}"

    def __repr__(self):
        if self.detailed:
            return f"BinaryOperation: {self.left} {self.operator} {self.right}"
        return f"BinaryOperation({self.left}, '{self.operator}', {self.right})"


class IfStatement(ASTNode):
    def __init__(self, condition, body):
        super().__init__("IF")
        self.condition = condition
        self.body = body

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

def parse(self):
    try:
        ast = self.parse_statement()
        if self.current_token < len(self.tokens) - 1:
            raise CustomSyntaxError("Unexpected token", 
                                    line=self.tokens[self.current_token].line,
                                    column=self.tokens[self.current_token].column)
        return ast
    
    except CustomSyntaxError as e:
        print(f"Syntax error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def parse_statement(self):
    if self.current_token >= len(self.tokens):
        raise CustomSyntaxError("Unexpected end of input")

    token = self.tokens[self.current_token]
    
    if token.token_type == TokenType.KEYWORD:
        keyword = token.value
        self.current_token += 1
        
        if keyword == 'if':
            return self.parse_if_statement()
        elif keyword == 'for':
            return self.parse_for_loop()
        elif keyword == 'func':
            return self.parse_function_declaration()
        # Add more cases for other keywords as needed...
        else:
            raise CustomSyntaxError(f"Unexpected keyword '{keyword}'", keyword)
    
    elif token.token_type == TokenType.IDENTIFIER:  # Assuming TOKEN_TYPE.IDENTIFIER exists
        self.current_token += 1
        return self.parse_variable_declaration()
    
    else:
        raise CustomSyntaxError(f"Expected keyword or identifier, got '{token.value}'", token)


def parse_if_statement(self):
    # Check for 'if' keyword
    if (self.current_token >= len(self.tokens) or 
            self.tokens[self.current_token][0] != 'KEYWORD' or 
            self.tokens[self.current_token][1] != 'if'):
        found_token = self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'end of input'
        raise ExpectedKeywordError('if', found_token)

    self.current_token += 1
    
    # Parse the condition
    condition = self.parse_expression()

    # Add a check for the condition validity
    if not condition:  # Assuming condition should not be None or some other validation logic
        raise InvalidConditionError()

    # Check for 'then' keyword after condition
    if (self.current_token >= len(self.tokens) or 
            self.tokens[self.current_token][0] != 'KEYWORD' or 
            self.tokens[self.current_token][1] != 'then'):
        found_token = self.tokens[self.current_token] if self.current_token < len(self.tokens) else 'end of input'
        raise ExpectedKeywordError('then', found_token)

    self.current_token += 1
    
    # Parse the body of the if statement
    body = self.parse_statement()

    return IfStatement(condition, body)
            
    def parse_for_loop(self):
        if self.current_token != 'KEYWORD' or self.tokens[self.current_token] != 'for':
            raise SyntaxError("Expected 'for' keyword")

        self.current_token += 1
        variable = self.parse_variable()

        if self.current_token != 'KEYWORD' or self.tokens[self.current_token] != 'in':
            raise SyntaxError("Expected 'in' keyword")

        self.current_token += 1
        iterable = self.parse_expression()

        if self.current_token != 'LOOP':
            raise SyntaxError("Expected 'loop'")

        self.current_token += 1
        body = self.parse_statement()

        return ASTNode("FOR_LOOP", variable, iterable, body)

    def parse_variable(self):
        try:
            token = self.tokens[self.current_token]
        except IndexError:
            raise VariableParseError("Error: No more tokens available to parse a variable.")

        if token.isalpha():  # Modify if you need to include other characters like `_`
            self.current_token += 1
            return token
        else:
            raise VariableParseError(f"Error: Expected variable, but got '{token}'", token)

    def parse_variable_declaration(self):
        if self.current_token != 'IDENTIFIER':
            raise SyntaxError("Expected identifier")
            variable = self.tokens[self.current_token]
            self.current_token += 1
            value = self.parse_expression()
            return f"{variable} = {value}"
        else:
            return variable

    def parse_program(self):
        program = []
        while self.current_toke != 'END':
            statement = self.parse_statement()
            program.append(statement)
        return program

    token = self.tokens[self.current_token]
    self.current_token += 1

    if token == 'KEYWORD':
        keyword = self.tokens[self.current_token - 1]
        if keyword == 'if':
            return self.parse_if_statement()
        elif keyword == 'for':
            return self.parse_for_loop()
        elif keyword == 'func':
            return self.parse_function_definition()
        # handle other keywords...
    elif token.isalpha():
        return self.parse_variable_declaration()
    else:
        raise SyntaxError(f"Expected keyword or identifier (got {token})")

    # Indentation level increased here
    # This code will be executed if the if-elif-else conditions are not met
    print("Default statement")
        
    def parse_function_declaration(self):
            if self.current_token != 'KEYWORD' or self.tokens[self.current_token] != 'func':
                raise SyntaxError("Expected 'func' keyword")
            self.current_token += 1
            function_name = self.parse_identifier()
            self.current_token += 1
            body = self.parse_statement()
            return ASTNode("FUNCTION", function_name, body)

    def parse_identifier(self):
            token = self.tokens[self.current_token]
            if token.isalpha():
                self.current_token += 1
                return token
            else:
                raise SyntaxError("Expected identifier")
        
    def parse_function_call(self):
            if self.current_token != 'IDENTIFIER':
                raise SyntaxError("Expected identifier")
            function_name = self.tokens[self.current_token]
            self.current_token += 1
            if self.current_token != '(':
                raise SyntaxError("Expected '(")
            arguments = []
            while True:
                argument = self.parse_expression()
                arguments.append(argument)
                if self.current_token == ')':
                    self.current_token += 1
                    break
                elif self.current_token == ',':
                    self.current_token += 1
                else:
                    raise SyntaxError("Expected ')' or ','")
            return ASTNode("FUNCTION_CALL", function_name, arguments)

    def parse_expression(self):
        token = self.tokens[self.current_token]
        if token.type in [TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER]:
            self.current_token += 1
            return token
        elif token.type == TokenType.LPAREN:
            return self.parse_function_call()
        elif token.type == TokenType.LBRACKET:
            return self.parse_array_access()

    def parse_array(self):
            if self.current_token != '[':
                raise SyntaxError("Expected '['")
            self.current_token += 1
            elements = []
            while True:
                element = self.parse_expression()
                elements.appens(element)
                if self.current_token == ']':
                    break
                elif self.current_token == ',':
                    self.current_token += 1
                else:
                    raise SyntaxError("Expected ']' or ','")
                    return ASTNode("ARRAY", elements)

    def parse_array_access(self):
            if self.current_token != '[':
                raise SyntaxError("Expected '[]")
            self.current_token += 1
            expression = self.parse_expression()
            if self.current_token != ']':
                raise SyntaxError("Expected ']'")
            return ASTNode("ARRAY_ACCESS", expression)

    def parse_class(self):
            if self.current_token != 'CLASS':
                raise SyntaxError("Expected 'CLASS' keyword")
            self.current_token += 1
            class_name = self.parse_identifier()
            self.current_token =+ 1
            body = self.parse_block()
            return ASTNode("CLASS_DEFINITION", class_name, body)

    def parse_object(self):
            if self.current_token != 'OBJECT':
                raise SyntaxError("Expected 'OBJECT' keyword")
            self.current_token += 1
            object_name = self.parse_identifier()
            self.current_token += 1
            properties = []
            while True:
                property_name = self.parse_identifier()
                property_value = self.parse_expression()
                properties.append((property_name, property_value))
                if self.current_token == '}':
                    break
                elif self.current_token == ',':
                    self.current_token += 1
                else:
                    raise SyntaxError("Expected '}' or ','")
            return ASTNode("OBJECT_DEFINITION", object_name, properties)

    def parse_class(self):
            if self.current_token != 'CLASS':
                raise SyntaxError("Expected 'CLASS' keyword")
            self.current_token += 1
            class_name = self.parse_identifier()
            self.current_token += 1
            if self.current_token == 'EXTENDS':
                inheritance = self.parse_inheritance()
                self.current_token += 1
            else:
                inheritance = None
            body; self.parse_block(self)
            return ASTNode("CLASS_DEFINITION", class_name, body, inheritance)

    def parse_block(self):
            self.consume('{')
            statements = []
            while True:
                statement = self.parse_stament()
                if statement is None:
                    break
                statements.append(statement)
            self.consume('}')
            return statements

    def parse_factor(self):
        token = self.tokens[self.current_token]
        if token['type'] == 'NUMBER':
            self.curent_token += 1
            return float(token['value'])
        elif token['type'] == 'IDENTIFIER':
            self.current_token += 1
            return token['value']
        elif token == '(':
            self.current_token += 1
            value = self.parse_expression()
            if self.current_token != ')':
                raise SyntaxError("Expected ')'")
            self.current_token += 1
            return value
        else:
            raise SyntaxError("Expected factor")

    def parse_term(self):
        left = self.parse_factor()
        while True:
            token = self.tokens[self.current_token]
            if token in ['**']:
                self.current_token += 1
                right = self.parse_factor()
                left = BinaryOperation(left, '**', right)
            elif token in ['+', '-']:
                self.current_token += 1
                left = UnaryOperation(token, left)
                break
            else:
                break
        return left
                
    # Put the parsing functions below this line. 