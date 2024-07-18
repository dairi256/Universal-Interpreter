class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def parse(self):
        ast = self.parse_statement()
        if self.current_token < len(self.tokens) - 1:
            raise SyntaxError("Unexpected token")
        return ast

    def parse_statement(self):
        if self.current_token >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")

    token = self.tokens[self.current_token]
    self.current_token += 1

    def parse_keyword(self, token):
        if token == 'KEYWORD':
            keyword = self.tokens[self.current_token - 1]
        if keyword == 'if':
            return self.parse_if_statement()
        elif keyword == 'for':
            return self.parse_for_loop()
        elif keyword == 'func':
            return self.parse_function_declaration()
        # add more cases for other keywords here...
        else:
            raise SyntaxError("Unexpected or expected keyword")


    def parse_if_statement(self):
        if self.current_token != 'KEYWORD' or self.tokens[self.current_token] != 'if':
            raise SyntaxError("expected 'if' keyword" )

        self.current_token += 1
        condition = self.parse_expresssion()
        if self.current_token != 'THEN':
            raise SyntaxError("Expected 'then'")
        self.current_token += 1
        body = self.parse_statement()

        return ASTNode("IF", condition, body)
            
    def parse_for_loop(self):
        if self.current_token != 'KEYWORD' or self.tokens[self.current_token] != 'for':
            raise SyntaxError("Expected 'for' keyword")

        self.current_token += 1
        variable = self.parse_variable()
        if self.current_token != 'LOOP':
            raise SyntaxError("Expected 'loop'")
        
        self.current_token += 1
        body = self.parse_statement()

        return ASTNode("FOR_LOOP", variable, iterable, body)

    def parse_expression(self):
        token = self.tokens[self.current_token]
        if token in ['NUMBER', 'STRING', 'IDENTIFIER']:
            self.current_token += 1
            return token
        elif token == '(':
            self.current_token += 1
            expression = self.parse_expression()
            if self.current_token != ')':
                raise SyntaxError("Expected ')'")

    def parse_variable(self):
        token = self.tokens[self.current_token]
        if token.isalpha():
            self.current_token += 1
            return token
        else:
            raise SyntaxError("Expected variable")

    def parse_variable_declaration(self):
        if self.current_token != 'IDENTIFIER':
            raise SyntaxError("Expected identifier")
            variable = self.tokens[self.current_token]
            self.current_token += 1
            value = self.parse_expression()
            return f"{variable} = {value}"
        else:
            return variable

def parse_statement(self):
    if self.current_token >= len(self.tokens):
        raise SyntaxError("Unexpected end of input")

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
            if token in ["NUMBER', 'STRING', 'IDENTIFIER'"]:
                expression = token
                self.current_token += 1
                return expression
            elif token == '(':
                expression = self.parse_function_call()
                return expression
            elif token == '[':
                expression = self.parse_array_access()
                return expression

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
    # Put the parsing functions below this line. 

class ASTNode:
    def __init__(self, token, *args):
        self.token = token
        if len(args) > 0:
            for arg in args:
                setattr(self, "value", arg)

    def __str__(self):
        if hasattr(self, "value"):
            return f"{self.token}({self.value})"
        else:
            return str(self.token)