from logic_formula_parser import lexer


def test_tokenize():
    data = "a&b|c|-d&-[]e|-<>-a->b"
    assert type(lexer.tokenize(data)) is list
