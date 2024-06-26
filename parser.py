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

        if token == 'KEYWORD':
            keyword = self.tokens[self.current_token - 1]
            if keyword == 'if':
                return self.parse_if_statement()
            elif keyword == 'for':
                return self.parse_for_loop()
                # handle other keywords..
        else:
            raise SyntaxError("Expected keyword")

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
                return self.parse_variable_declaration()
                # handle other keywords..
        elif token.isalpha():
            return self.parse_variable_declaration()
        else:
            raise SyntaxError("Expected keyword or identifier")
        
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
    # use this line or more lines to implement other parsing functions.

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