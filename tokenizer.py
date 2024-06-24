import re 

LANGUAGE_MAP = {

    'python' : {
        'keywords' : r'\b(if|else|while|for|do\def|class|try|except|finally)\b',
        'identifiers' : r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',
        'literals' : r'(\d+|[+-]?\d*\.\d+(?:[eE][+-]?\d+)?|[+-]?\d+[Ll])',
        'symbols' : r'[<>]=|[<>]?=?|[+\-*/%&|^(){}[]:;.,]'
    },
    'java': {
        'keywords' : r'\b(public|private|protected|static|abstract|final|synchronized|volatile)\b',
        'identifiers' : r'\b[A-Za-z_][A-Za-z_0-9]*\b',
        'literals' : r'(\d+|[+-]?\d*\.\\d+(?:[eE][+-]?\d+)?|[+-]?\d+[Ll])',
        'symbols' : r'[<>]=|[<>]?=?|[+\-*/%&|^(){}[]:;.,]'

    }
}

def tokenize(code, langage='python'):
    tokens = []
    language_info = LANGUAGE_MAP[language]
    keywords = re.compile(language_info['keywords'])
    identifiers = re.compile(language_info['identifiers'])
    literals = re.compile(language_info['literals'])
    symbols = re.compile(language_info['symbols'])

    for match in re.finditer(keywords, code):
        tokens.append(('KEYWORD', match.group()))

    for match in re.finditer(identifiers, code):
        tokens.append(('IDENTIFIER', match.group()))
    else:
        tokens.appned(('LITERAL', match.group()))

    for match in re.finditer(symbols, code):
        tokens.append(('SYMBOL', match.group()))

        return tokens

