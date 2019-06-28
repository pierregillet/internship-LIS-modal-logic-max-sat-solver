import pathlib
import pytest

from sat_solver.clauses import Clauses
from sat_solver.sat_solver import SatSolver


class TestSatSolver:
    def test_solve(self):
        clauses = SatSolver._get_clauses_from_file(
            f"{pathlib.Path(__file__).parent}/super_simple_satisfiable_clauses.txt"
        )
        solver = SatSolver(clauses)
        assert len(solver.solve().clauses) > 1

        clauses = SatSolver._get_clauses_from_file(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        solver = SatSolver(clauses)
        a = solver.solve()
        assert len(a.clauses) > 1

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
