import re

LANGUAGE_MAP = {
    'python': {
        'keywords': r'\b(if|else|while|for|do\def|class|try|except|finally)\b',
        'identifiers': r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',
        'literals': r'(\d+|[+-]?\d*\.\\d+(?:[eE][+-]?\d+)?|[+-]?\d+[Ll])',
        'symbols': r'[<>]=|[<>]?=?|[+\-*/%&|^(){}[]:;.,]',
        'multi_line_comment': r'(?s)(?L#.*?)(?:\n|$)'
    },
    'java': {
        'keywords': r'\b(public|private|protected|static|abstract|final|synchronized|volatile)\b',
        'identifiers': r'\b[A-Za-z_][A-Za-z_0-9]*\b',
        'literals': r'(\d+|[+-]?\d*\.\\d+(?:[eE][+-]?\d+)?|[+-]?\d+[Ll])',
        'symbols': r'[<>]=|[<>]?=?|[+\-*/%&|^(){}[]:;.,]'
    }
}

def tokenize(code, language='python'):
    language_info = LANGUAGE_MAP.get(language)
    keywords = re.compile(language_info['keywords'])
    identifiers = re.compile(language_info['identifiers'])
    literals = re.compile(language_info['literals'])
    symbols = re.compile(language_info['symbols'])
    multi_line_comment = re.compile(r'\/\*.*?\*\/', re.DOTALL)

    tokens = []
    in_comment = False
    comment = ''
    for char in code:
        if char == '/':
            if not in_comment:
                if code[code.index(char) + 1] == '*':
                    in_comment = True
                    continue
            else:
                if code[code.index(char) + 1] == '/':
                    in_comment = False
                    continue
        elif in_comment:
            comment += char
            continue

        if match := keywords.match(code, pos=code.index(char)):
            tokens.append(('KEYWORD', match.group()))
            continue
        elif match := identifiers.match(code, pos=code.index(char)):
            tokens.append(('IDENTIFIER', match.group()))
            continue
        elif match := literals.match(code, pos=code.index(char)):
            tokens.append(('LITERAL', match.group()))
            continue
        elif match := symbols.match(code, pos=code.index(char)):
            tokens.append(('SYMBOL', match.group()))
            continue

    highlighted_code = ''
    for token in tokens:
        if token[0] == 'KEYWORD':
            highlighted_code += f'**{token[1]}** '
        elif token[0] == 'LITERAL':
            highlighted_code += f'{token[1]} '
        else:
            highlighted_code += f'{token[1]} '
    return {'tokens': tokens, 'highlighted_code': highlighted_code.strip()}