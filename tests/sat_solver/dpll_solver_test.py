import pathlib
import pytest

from sat_solver.dpll_solver import DpllSatSolver


class TestDpllSatSolver:
    # @pytest.mark.skip(reason="Not yet implemented")
    def test_solve(self):
        solver = DpllSatSolver.from_file(
            f"{pathlib.Path(__file__).parent}/super_simple_satisfiable_clauses.txt"
        )
        assert len(solver.solve().clauses) > 1

        solver = DpllSatSolver.from_file(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        a = solver.solve()
        assert len(a.clauses) > 1
