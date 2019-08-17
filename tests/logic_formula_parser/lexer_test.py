from logic_formula_parser import lexer


def test_tokenize():
    data = "a&b|c|-d&-[H]e|-H-a->Lbonjour"
    result = lexer.tokenize(data)
    assert isinstance(result, list)
