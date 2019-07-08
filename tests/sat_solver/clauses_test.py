import pytest

from sat_solver.clauses import Clauses


class TestClauses:
    def test_is_mono_literal(self):
        multi_literal = {-1, -3, -1}
        assert Clauses.is_mono_literal(multi_literal) is False
        mono_literal = {-1}
        assert Clauses.is_mono_literal(mono_literal) is True

    def test__unit_propagate(self):
        clauses = Clauses.from_int([
            {1, 2},
            {-1, -2},
            {2, 3, 4},
            {-1, -3},
        ])
        expected = [{-3, -1}, {-1}]
        clauses.unit_propagate(2)
        assert clauses.clauses == expected

    def test_contains_only_mono_literals(self):
        multi_literal = {-1, -3, -1}
        assert Clauses.is_mono_literal(multi_literal) is False
        mono_literal = {-1}
        assert Clauses.is_mono_literal(mono_literal) is True

    def test__find_pure_literals(self):
        clauses = Clauses.from_int([
            {-1, -3},
            {-2, 1, 5},
            set(),
            {-1},
        ])
        pure_literals = {-2, -3, 5}
        assert clauses.find_pure_literals() == pure_literals

    @pytest.mark.skip(reason="Not yet implemented")
    def test_find_mono_literals(self):
        assert False

    @pytest.mark.skip(reason="Not yet implemented")
    def test_is_consistant_set_of_literals(self):
        assert False

    @pytest.mark.skip(reason="Not yet implemented")
    def test_convert_literals_to_integers(self):
        assert False

    @pytest.mark.skip(reason="Not yet implemented")
    def test_contains_empty_clause(self):
        assert False
