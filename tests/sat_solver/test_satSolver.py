import pathlib
from unittest import TestCase

from sat_solver.sat_solver import SatSolver


class TestSatSolver(TestCase):
    # def test_solve(self):
    #     self.fail()

    def test__get_formatted_clauses_from_file(self):
        sat_solver: SatSolver = SatSolver(
            f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
        )
        formatted_clauses = sat_solver._get_formatted_clauses_from_file()
        self.assertEqual(formatted_clauses, [
            ["a", "b", "¬", "→"], ["b", "¬", "c", "→"], ["c", "a", "→"],
            ["a", "b", "¬", "∨", "c", "∨"],
        ])

        sat_solver: SatSolver = SatSolver(
            f"{pathlib.Path(__file__).parent}/unsatisfiable_clauses.txt"
        )
        formatted_clauses = sat_solver._get_formatted_clauses_from_file()
        self.assertEqual(formatted_clauses, [
            ["a", "b", "→"], ["b", "c", "→"], ["c", "a", "→"],
            ["a", "b", "∨", "c", "∨"],
            ["a", "¬", "b", "¬", "∨", "c", "¬", "∨"],
        ])


    # def test__find_mono_literals(self):
    #     self.fail()
