from typing import *
from ply import lex

tokens = (
    "NOT",
    "BOX",
    "DIAMOND",
    "AND",
    "OR",
    "IMPLY",
    # "LPAREN",
    # "RPAREN",
    "PROPOSITION",
)

t_NOT = r'-'
t_BOX = r'\[\]'
t_DIAMOND = r'<>'
t_AND = r'&'
t_OR = r'\|'
t_IMPLY = r'->'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
t_PROPOSITION = r'\w+'


def t_COMMENT(t):
    r'\#.*'
    pass  # No return value. Token discarded


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# lexer = lex.lex(debug=1)
lexer = lex.lex()

if __name__ == "__main__":
    # data = "a&b|(c|-d&-[]e|-<>-a->b)"
    data = "a&b"
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
