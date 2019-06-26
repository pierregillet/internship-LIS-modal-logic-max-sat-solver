from typing import *
import pytest

from sat_solver.clauses import Clauses


class TestClauses:
    def test_is_mono_literal(self):
        multi_literal = frozenset([-1, -3, -1])
        assert Clauses.is_mono_literal(multi_literal) == False
        mono_literal: FrozenSet[int] = frozenset({-1})
        assert Clauses.is_mono_literal(mono_literal) == True

    def test_contains_only_mono_literals(self):
        multi_literal = frozenset([-1, -3, -1])
        assert Clauses.is_mono_literal(multi_literal) is False
        mono_literal: FrozenSet[int] = frozenset({-1})
        assert Clauses.is_mono_literal(mono_literal) is True

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
