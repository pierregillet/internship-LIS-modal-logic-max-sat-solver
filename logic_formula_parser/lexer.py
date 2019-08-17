from typing import *
from ply import lex

tokens = (
    "NOT",
    "L",  # System T box
    "HBOX",  # System K box
    "H",  # System K diamond
    "AND",
    "OR",
    "IMPLY",
    # "LPAREN",
    # "RPAREN",
    "PROPOSITION",
)

t_HBOX = r'\[H\]'
t_L = r'L'
t_H = r'H'
t_IMPLY = r'->'
t_AND = r'&'
t_OR = r'\|'
t_PROPOSITION = r'[a-z0-9]\w*'
t_NOT = r'-'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'


def t_COMMENT(t):
    r'\#.*'
    pass  # No return value. Token discarded


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def tokenize(data):
    lexer.input(data)
    return [token for token in lexer]


# lexer = lex.lex(debug=1)
lexer = lex.lex()
