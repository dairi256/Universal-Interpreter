import re
import string

LANGUAGE_MAP = {
    'python': {
        'keywords': r'\b(replace|with|from|import|class|def|if|else|elif|while|for|in|not|and|or|xor|is|isnt|in\W+|\W+in)\b',
        'identifiers': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'literals': r"[rR]\"([^\"]|[\\\"]|[^\"])*\"|[rR]'([^\']|[\\\']|[^\'])*\'|[rR]\['([^\']|[\\\']|[^\'])*'\]\"",
        'symbols': r'[' + re.escape(string.punctuation) + ']'
    }
}

def tokenize(code, language='python'):
    language_info = LANGUAGE_MAP.get(language)
    keywords = re.compile(language_info['keywords'], re.UNICODE)
    identifiers = re.compile(language_info['identifiers'], re.UNICODE)
    literals = re.compile(language_info['literals'], re.UNICODE)
    symbols = re.compile(language_info['symbols'], re.UNICODE)
    multi_line_comment = re.compile(r'\/\*.*?\*\/', re.DOTALL)
    single_line_comment = re.compile(r'\/\/.*$')
    unicode_escape_sequence = re.compile(r'\\u[0-9a-fA-F]{4}')
    whitespace = re.compile(r'\s+')

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

        if match := single_line_comment.match(code):
            tokens.append(('COMMENT', match.group()))
            continue

        if match := keywords.match(code):
            tokens.append(('KEYWORD', match.group()))
            continue
        elif match := identifiers.match(code):
            tokens.append(('IDENTIFIER', match.group()))
            continue
        elif match := literals.match(code):
            if match.group().startswith('r"') or match.group().startswith('r\''):
                tokens.append(('LITERAL', match.group()))
                continue
            else:
                tokens.append(('STRING_LITERAL', match.group().strip('"\'')))
                continue
        elif match := symbols.match(code):
            if match.group() == '\\':
                if match := unicode_escape_sequence.match(code[code.index(char) + 1]):
                    tokens.append(('SYMBOL', match.group()))
                    continue
            else:
                tokens.append(('SYMBOL', match.group()))
                continue

        if match := whitespace.match(code):
            tokens.append(('WHITESPACE', match.group()))
            continue

    highlighted_code = ''
    for token in tokens:
        if token[0] == 'KEYWORD':
            highlighted_code += f'**{token[1]}** '
        elif token[0] == 'LITERAL':
            highlighted_code += f'{token[1]} '
        elif token[0] == 'STRING_LITERAL':
            highlighted_code += f"'{token[1]}' "
        elif token[0] == 'WHITESPACE':
            highlighted_code += f'{token[1]} '
        elif token[0] == 'COMMENT':
            highlighted_code += f'# {token[1]} '
        else:
            highlighted_code += f'{token[1]} '
    return {'tokens': tokens, 'highlighted_code': highlighted_code.strip()}