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
        # code for parse if statement
        pass
    
    def parse_for_loop(self):
        # code for parse for loop
        pass
    
    # use this line or more lines to implement other parsing functions.

class ASTNode:
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return str(self.token)