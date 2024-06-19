import re 

def tokenize(code):
    tokens = []
    keywords = r'\b(if|else|while|for|do|else)\b'
    for match in re.finditer(keywords, code):
        tokens.append(('KEYWORD', match.group()))

    identifiers = r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'
    for match in re.finditer(identifiers, code):
        tokens.append(('IDENTIFIER', MATCH.GROUP()))

    literals = r'(\d+|[+-]?\d*.\d+(?:[eE][+-]?\d+)?[+-?\d+[Ll]])'
    for match in re.finditer(literals, code):
        tokens.append(('IDENTIFIER', match.group()))

    symbols = r'[<>]=|[<>]?=?|[+\-*/%&|^(){}[]:;.,]'
    for match in re.finditer(symbols, code):
        tokens.append(('SYMBOL', match.group()))

    return tokens


code = "x = 5 + 3 * 2"
tokens = tokenize(code)
print(tokens)