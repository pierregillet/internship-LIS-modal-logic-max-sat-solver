from ply import yacc

# Get the token map from the lexer.  This is required.
from logic_formula_parser.lexer import lexer, tokenize, tokens
import logic_formula_parser.operators as op

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


def p_term_not(p):
    'term : NOT proposition'
    p[0] = op.Not(p[2])


def p_term_var(p):
    'term : proposition'
    p[0] = p[1]


def p_proposition_box_not(p):
    'proposition : BOX NOT PROPOSITION'
    p[0] = op.BoxNot(op.Proposition(p[3]))


def p_proposition_diamond_not(p):
    'proposition : DIAMOND NOT PROPOSITION'
    p[0] = op.DiamondNot(op.Proposition(p[3]))


def p_proposition_box(p):
    'proposition : BOX PROPOSITION'
    p[0] = op.Box(op.Proposition(p[2]))


def p_proposition_diamond(p):
    'proposition : DIAMOND PROPOSITION'
    p[0] = op.Diamond(op.Proposition(p[2]))


def p_proposition_proposition(p):
    'proposition : PROPOSITION'
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
    # data = "a&b|c|-d&-[]e|-<>-a->b"
    data = "-a|[]-b"
    result = parse(data)
    print(result)
