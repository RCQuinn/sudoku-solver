# Standard library imports
import tkinter as tk
from math import sqrt
from typing import List

# Local imports
from sudoku_solver.classes.view import View
from sudoku_solver.classes.model import Model

PLACEHOLDER: int = 0            # The 0 value is merely symbolic. Could be anything other than 1->9 .
_TGrid = List[List[int]]        # Custom hint for Type Hinting.


class Controller:
    """A Class used to interface between Model and View layers.
    Responds to user input from the View, and delegations from the Model.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.model = Model(self)
        self.view = View(self)

        # Initialize objects in view
        self.view.set_label_text("Ready")

    def quit_button_pressed(self) -> None:
        """Close the window."""
        self.root.destroy()

    def puzzle_changed_delegate(self) -> None:
        """Model internally changes and needs to signal the change."""
        solution = self.model.get_solution()
        problem = self.model.get_problem()

        # Flatten 2D list to 1D and send to View
        if solution is not None and problem is not None:
            flat_solution = [val for sublist in solution for val in sublist]
            flat_problem = [val for sublist in problem for val in sublist]
            self.view.set_entry_grid(flat_solution, flat_problem)
            self.view.set_label_text("Solution found!")
        else:
            self.view.set_label_text("Unable to find solution.")

    def send_data(self, user_input: List[tk.Entry]) -> None:
        """Transform and send data to Model."""
        values = self.get_values(user_input)
        new_values = self.convert_values(values)
        grid = self.list_to_square(new_values)

        if self.validate_user_grid(grid):
            self.model.solve(grid)
        else:
            self.view.set_label_text("Invalid puzzle. Check values again.")

    def clear(self) -> None:
        """Re-initialise View."""
        self.view.clear_grid()
        self.view.set_label_text("Ready")

    @staticmethod
    def validateEntry(i: str, S: str) -> bool:
        """ Allow ONLY numbers 1->9 and exactly 1 character in length."""
        if S in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and int(i) == 0:
            return True
        return False

    @staticmethod
    def get_values(entries: List[tk.Entry]) -> List[str]:
        """Extract values from the Entry objects."""
        return [entry.get() for entry in entries]  # Get values from the entry.

    @staticmethod
    def convert_values(values: List[str]) -> List[int]:
        """Replaces empty strings with a placeholder and converts non-empty values to integers."""
        new_values = []
        for value in values:
            if value == '':
                new_values.append(PLACEHOLDER)
            else:
                new_values.append(int(value))
        return new_values

    @staticmethod
    def list_to_square(values: List[int]) -> _TGrid:
        """Converts a 1D list to a 2D list where row and column values are identical.
        Assumes the length of the input is a perfect square.
        """
        width = int(sqrt(len(values)))  # In the event of a non perfect square length, truncates.
        return [values[i:i + width] for i in range(0, len(values), width)]  # Convert 1D to 2D

    @staticmethod
    def validate_user_grid(grid: _TGrid) -> bool:
        """Checks the entire Sudoku grid for illegal values."""

        def contains_duplicates(lst: List[int]) -> bool:
            x = [value for value in lst if value != PLACEHOLDER]  # Remove placeholder value
            return len(set(x)) != len(x)  # If not match then there is a duplicate

        # Check each row for duplicate values
        for row in range(9):
            if contains_duplicates(grid[row]):
                return False

        # Check each column for duplicate values
        for col in range(9):
            swapped_grid = [sublist[col:col + 1][0] for sublist in grid]
            if contains_duplicates(swapped_grid):
                return False

        # Check each sub grid for duplicate values
        for rc in range(1, 10, 3):
            for cc in range(1, 10, 3):
                # Takes center of each sub grid and manually gets surrounding values.
                sub_grid = [grid[rc - 1][cc - 1], grid[rc - 1][cc], grid[rc - 1][cc + 1],
                            grid[rc][cc - 1], grid[rc][cc], grid[rc][cc + 1],
                            grid[rc + 1][cc - 1], grid[rc + 1][cc], grid[rc + 1][cc + 1]
                            ]
                if contains_duplicates(sub_grid):
                    return False
        return True
