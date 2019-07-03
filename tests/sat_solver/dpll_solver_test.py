import pathlib

from dpll_solver import SatSolver


class TestSatSolver:
    def test_solve(self):
        solver = SatSolver.from_file(
            f"{pathlib.Path(__file__).parent}/super_simple_satisfiable_clauses.txt"
        )
        assert len(solver.solve().clauses) > 1

        solver = SatSolver.from_file(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        assert len(solver.solve().clauses) > 1
