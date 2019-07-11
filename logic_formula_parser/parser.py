from ply import yacc

# Get the token map from the lexer.  This is required.
from lexer import lexer, tokens
import operators as op

precedence = (
    ("left", "IMPLY"),
    ("left", "OR"),
    ("left", "AND"),
    ("right", "NOT", "BOX", "DIAMOND")
)


def p_formula_imply(p):
    'formula : formula IMPLY formula'
    p[0] = op.Imply(p[1], p[3])


def p_formula_or(p):
    'formula : formula OR formula'
    p[0] = op.Or(p[1], p[3])


def p_formula_and(p):
    'formula : formula AND formula'
    p[0] = op.And(p[1], p[3])


def p_formula_term(p):
    'formula : term'
    p[0] = p[1]


def p_term_box_not(p):
    'term : BOX NOT proposition'
    p[0] = op.BoxNot(p[3])


def p_term_diamond_not(p):
    'term : DIAMOND NOT proposition'
    p[0] = op.DiamondNot(p[2])


def p_term_box(p):
    'term : BOX proposition'
    p[0] = op.Box(p[2])


def p_term_diamond(p):
    'term : DIAMOND proposition'
    p[0] = op.Diamond(p[2])


def p_term_var(p):
    'term : proposition'
    p[0] = p[1]


def p_proposition_proposition(p):
    'proposition : PROPOSITION'
    p[0] = op.Proposition(p[1])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print(p)


if __name__ == "__main__":
    # data = "a&b|c|-d&-[]e|-<>-a->b"
    data = "a|[]-b"
    lexer.input(data)
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break      # No more input
    #     print(tok)

    yacc.yacc(write_tables=True, debug=True)
    parser = yacc.yacc()
    result = parser.parse(data, lexer=lexer)
    print(result)

    # while True:
    #     try:
    #         # s = input('calc > ')
    #         s = input('calc > ')
    #     except EOFError:
    #         break
    #     if not s:
    #         continue
