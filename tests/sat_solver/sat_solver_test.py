import pathlib
import pytest

from sat_solver.clauses import Clauses
from sat_solver.sat_solver import SatSolver


class TestSatSolver:
    @pytest.mark.skip(reason="Not yet implemented")
    def test_solve(self):
        assert False

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
        assert clauses.clauses == expected.clauses

        clauses = SatSolver._get_clauses_from_file(
            f"{pathlib.Path(__file__).parent}/unsatisfiable_clauses.txt"
        )
        expected = Clauses.from_int(frozenset({
            frozenset({-1, 2}),
            frozenset({-2, 3}),
            frozenset({-3, 1}),
            frozenset({1, 2, 3}),
            frozenset({-1, -2, -3}),
        }))
        assert clauses.clauses == expected.clauses

    def test__find_pure_literals(self):
        clauses = Clauses.from_int(
            frozenset({frozenset({-1, -3}),
                       frozenset({-2, 1, 5}),
                       frozenset({}),
                       frozenset({-1})})
        )
        pure_literals = {-2, -3, 5}
        assert SatSolver._find_pure_literals(clauses) == pure_literals
