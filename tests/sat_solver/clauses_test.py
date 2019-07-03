from typing import *
import pytest

from clauses import Clauses


class TestClauses:
    def test_is_mono_literal(self):
        multi_literal = frozenset([-1, -3, -1])
        assert Clauses.is_mono_literal(multi_literal) is False
        mono_literal: FrozenSet[int] = frozenset({-1})
        assert Clauses.is_mono_literal(mono_literal) is True

    def test__unit_propagate(self):
        clauses = Clauses.from_int(frozenset({
            frozenset({1, 2}),
            frozenset({-1, -2}),
            frozenset({2, 3, 4}),
            frozenset({-1, -3}),
        }))
        expected = frozenset({
            frozenset({-1}),
            frozenset({-1, -3}),
        })
        assert clauses.unit_propagate(2).clauses == expected

    def test_contains_only_mono_literals(self):
        multi_literal = frozenset({-1, -3, -1})
        assert Clauses.is_mono_literal(multi_literal) is False
        mono_literal: FrozenSet[int] = frozenset({-1})
        assert Clauses.is_mono_literal(mono_literal) is True

    def test__find_pure_literals(self):
        clauses = Clauses.from_int(
            frozenset({frozenset({-1, -3}),
                       frozenset({-2, 1, 5}),
                       frozenset({}),
                       frozenset({-1})})
        )
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
