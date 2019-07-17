import pathlib
import pytest

from sat_solver.dpll_solver import DpllSatSolver


class TestDpllSatSolver:
    @pytest.mark.skip(reason="Refactoring")
    def test_solve(self):
        solver = DpllSatSolver.from_file(
            f"{pathlib.Path(__file__).parent}"
            f"/super_simple_satisfiable_clauses.txt"
        )
        assert len(solver.solve().clauses) > 1

        solver = DpllSatSolver.from_file(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        assert len(solver.solve().clauses) > 1
