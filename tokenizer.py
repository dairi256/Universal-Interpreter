import re 

LANGUAGE_MAP = {

    'python' : {
        'keywords' : r'\b(if|else|while|for|do\def|class|try|except|finally)\b',
        'identifiers' : r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',
        'literals' : r'(\d+|[+-]?\d*\.\d+(?:[eE][+-]?\d+)?|[+-]?\d+[Ll])',
        'symbols' : r'[<>]=|[<>]?=?|'