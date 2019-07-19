import pathlib
import pytest

from sat_solver.dpll_solver import DpllSatSolver


class TestDpllSatSolver:
    def test_solve(self):
        solver = DpllSatSolver.from_file(
            f"{pathlib.Path(__file__).parent}"
            f"/super_simple_satisfiable_clauses.txt"
        )
        solution = solver.solve()
        assert solution and len(solution.clauses) > 1

        solver = DpllSatSolver.from_file(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        solution = solver.solve()
        assert solution and len(solver.solve().clauses) > 1
