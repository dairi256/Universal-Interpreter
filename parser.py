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
    # use this line or more lines to implement other parsing functions.

class ASTNode:
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return str(self.token)