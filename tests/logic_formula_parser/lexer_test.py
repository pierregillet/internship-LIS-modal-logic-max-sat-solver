from logic_formula_parser import lexer


def test_tokenize():
    data = "a&b|c|-d&-[]e|-<>-a->b"
    result = lexer.tokenize(data)
    assert isinstance(result, list)
