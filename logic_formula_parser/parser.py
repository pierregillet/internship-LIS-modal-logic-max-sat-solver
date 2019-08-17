from ply import yacc

# Get the token map from the lexer. This is required.
from logic_formula_parser.lexer import lexer, tokenize, tokens
import logic_formula_parser.operators as op

precedence = (
    ("left", "IMPLY"),
    ("left", "OR"),
    ("left", "AND"),
    ("right", "HBOX", "L", "H"),
    ("right", "NOT")
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


def p_formula(p):
    'formula : term'
    p[0] = p[1]


def p_term_not(p):
    'term : NOT leaf'
    p[0] = op.Not(p[2])


def p_term(p):
    'term : leaf'
    p[0] = p[1]


def p_leaf_hbox_not(p):
    'leaf : HBOX NOT PROPOSITION'
    p[0] = op.HBox(op.Not(op.Proposition(p[3])))


def p_leaf_hbox(p):
    'leaf : HBOX PROPOSITION'
    p[0] = op.HBox(op.Proposition(p[2]))


def p_leaf_not_h(p):
    'leaf : H NOT PROPOSITION'
    p[0] = op.H(op.Not(op.Proposition(p[3])))


def p_leaf_h(p):
    'leaf : H PROPOSITION'
    p[0] = op.H(op.Proposition(p[2]))


def p_leaf_l_not(p):
    'leaf : L NOT PROPOSITION'
    p[0] = op.LNot(op.Proposition(p[3]))


def p_leaf_l(p):
    'leaf : L PROPOSITION'
    p[0] = op.L(op.Proposition(p[2]))


def p_leaf(p):
    'leaf : PROPOSITION'
    p[0] = op.Proposition(p[1])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print(p)


def parse_file(filename: str):
    with open(filename) as f:
        for line in f:
            tokenize(line)
            parser = yacc.yacc()
            parser.parse(line, lexer=lexer)
    return


def parse(data: str):
    # yacc.yacc(write_tables=True, debug=True)
    parser = yacc.yacc()
    return parser.parse(data, lexer=lexer)


if __name__ == "__main__":
    # formula = "a&b|c|-d&-[H]e|-L-a->b"
    formula = "-a|[H]-b&L"
    result = parse(formula)
    print(result)
