import re
import string

LANGUAGE_MAP = {
    'python': {
        'keywords': r'\b(replace|with|from|import|class|def|if|else|elif|while|for|in|not|and|or|xor|is|isnt|in\W+|\W+in)\b',
        'identifiers': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'literals': r"[rR]\"([\\\"]|[^\"])*\"|[rR]'([\\']|[^\'])*'",
        'symbols': r'[' + re.escape(string.punctuation) + ']'
    }
}

def tokenize(code, language='python'):
    language_info = LANGUAGE_MAP.get(language)
    keywords = re.compile(language_info['keywords'])
    identifiers = re.compile(language_info['identifiers'])
    literals = re.compile(language_info['literals'])
    symbols = re.compile(language_info['symbols'])
    multi_line_comment = re.compile(r'\/\*.*?\*\/', re.DOTALL)
    escape_sequence = re.compile(r'\\.')

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
            if match.group().startswith('r"') or match.group().startswith('r\''):
                tokens.append(('LITERAL', match.group()))
                continue
            else:
                tokens.append(('STRING_LITERAL', match.group().strip('"\'')))
                continue
        elif match := symbols.match(code, pos=code.index(char)):
            if match.group() == '\\':
                if match := escape_sequence.match(code[code.index(char) + 1]):
                    tokens.append(('SYMBOL', match.group()))
                    continue
            else:
                tokens.append(('SYMBOL', match.group()))
                continue

    highlighted_code = ''
    for token in tokens:
        if token[0] == 'KEYWORD':
            highlighted_code += f'**{token[1]}** '
        elif token[0] == 'LITERAL':
            highlighted_code += f'{token[1]} '
        elif token[0] == 'STRING_LITERAL':
            highlighted_code += f"'{token[1]}' "
        else:
            highlighted_code += f'{token[1]} '
    return {'tokens': tokens, 'highlighted_code': highlighted_code.strip()}