from typing import *
import unittest

from sat_solver.clauses import Clauses


class TestClauses(unittest.TestCase):
    def test_is_mono_literal(self):
        multi_literal = frozenset([-1, -3, -1])
        self.assertEqual(
            Clauses.is_mono_literal(multi_literal), False
        )
        mono_literal: FrozenSet[int] = frozenset({-1})
        self.assertEqual(
            Clauses.is_mono_literal(mono_literal), True
        )

    def test_contains_only_mono_literals(self):
        multi_literal = frozenset([-1, -3, -1])
        self.assertEqual(
            Clauses.is_mono_literal(multi_literal), False
        )
        mono_literal: FrozenSet[int] = frozenset({-1})
        self.assertEqual(
            Clauses.is_mono_literal(mono_literal), True
        )

    @unittest.skip("Not yet implemented")
    def test_find_mono_literals(self):
        self.fail()

    @unittest.skip("Not yet implemented")
    def test_is_consistant_set_of_literals(self):
        self.fail()

    @unittest.skip("Not yet implemented")
    def test_convert_literals_to_integers(self):
        self.fail()

    @unittest.skip("Not yet implemented")
    def test_contains_empty_clause(self):
        self.fail()
