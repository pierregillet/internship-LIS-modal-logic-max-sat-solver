import pathlib
import unittest

from sat_solver.clauses import Clauses
from sat_solver.sat_solver import SatSolver


class TestSatSolver(unittest.TestCase):
    @unittest.skip("Not yet implemented")
    def test_solve(self):
        self.fail()

    @unittest.skip("TODO: fix this test")
    def test__get_clauses_from_file(self):
        clauses = SatSolver._get_clauses_from_file(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        expected = Clauses.from_int(frozenset({
            frozenset({-1, -2}),
            frozenset({2, 3}),
            frozenset({-3, 1}),
            frozenset({1, -2, 3}),
        }))
        self.assertEqual(
            clauses.clauses,
            expected.clauses)

        # clauses = SatSolver._get_clauses_from_file(
        #     f"{pathlib.Path(__file__).parent}/unsatisfiable_clauses.txt"
        # )
        # self.assertEqual(clauses.clauses, frozenset({
        #     ("a", "b", "→"), ("b", "c", "→"), ("c", "a", "→"),
        #     ("a", "b", "∨", "c", "∨"),
        #     ("a", "¬", "b", "¬", "∨", "c", "¬", "∨"),
        # }))

    def test__find_pure_literals(self):
        clauses = Clauses.from_int(
            frozenset({frozenset({-1, -3}),
                       frozenset({-2, 1, 5}),
                       frozenset({}),
                       frozenset({-1})})
        )
        pure_literals = {-2, -3, 5}
        self.assertEqual(SatSolver._find_pure_literals(clauses), pure_literals)
