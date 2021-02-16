# PEP 563 -- Postponed Evaluation of Annotations. Avoids circular imports.
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller

# Standard library imports
from typing import List, Optional

_TGrid = List[List[int]]        # Custom hint for Type Hinting.


class Model:
    """Calculates a complete Sudoku based off an incomplete puzzle."""
    def __init__(self, vc: Controller) -> None:
        self.vc = vc
        self.solution = None    # type: Optional[_TGrid]
        self.problem = None     # type: Optional[_TGrid]

    # Delegates-- Model would call this on internal change
    def puzzle_changed(self) -> None:
        """Function to call when Model has an internal change."""
        self.vc.puzzle_changed_delegate()

    def get_solution(self) -> Optional[_TGrid]:
        """Return the solved grid, or None if it does not exist."""
        return self.solution

    def get_problem(self) -> Optional[_TGrid]:
        """Return the user-provided grid, or None if it does not exist."""
        return self.problem

    def solve(self, grid: _TGrid) -> None:
        """Entry point to the backtracking algorithm."""
        self.problem = [x[:] for x in grid]     # Take copy of original grid
        self.solution = self.backtracking(grid, 0, 0)
        self.puzzle_changed()

    def backtracking(self, grid: _TGrid, row_index: int, col_index: int) -> Optional[_TGrid]:
        """Tries incrementally possible solutions until either a fully completed grid is found,
        or progress cannot be made; in which cases backtrack to the last feasible value and keep going.
        """
        # Exit condition is true when row_index and col_index is equal to 8
        if row_index == 9 and col_index == 0:
            return grid

        # Check each blank space
        if grid[row_index][col_index] == 0:
            for value in range(1, 10):
                if not self.is_invalid(grid, row_index, col_index, value):
                    # If valid, set and proceed to next space
                    grid[row_index][col_index] = value
                    if self.next_space(grid, row_index, col_index):
                        return grid
            # No valid values, reset space
            grid[row_index][col_index] = 0

        # If this space is full, proceed
        else:
            if self.next_space(grid, row_index, col_index):
                return grid

        return None

    def next_space(self, grid: _TGrid, row_index: int, col_index: int) -> Optional[_TGrid]:
        """Called by backtracking function. Continues recursion on next line of grid, if applicable."""
        if col_index == 8:  # If row finishes, go to next line.
            col_index = 0
            return self.backtracking(grid, row_index + 1, col_index)
        else:
            return self.backtracking(grid, row_index, col_index + 1)

    @staticmethod
    def is_invalid(grid: _TGrid, row_index: int, col_index: int, value: int) -> bool:
        """ Checks for duplicate values in the current row, column, and sub grid."""

        def check_row() -> bool:
            for column in range(9):
                if grid[row_index][column] == value:
                    return True
            return False

        def check_column() -> bool:
            for row in range(9):
                if grid[row][col_index] == value:
                    return True
            return False

        def check_sub_grid() -> bool:
            row_corner = row_index - (row_index % 3)  # Find top corner of grid
            col_corner = col_index - (col_index % 3)  # for row and column.
            for r in range(row_corner, row_corner + 3):
                for c in range(col_corner, col_corner + 3):
                    if grid[r][c] == value:
                        return True
            return False

        # If ANY match is found, that value is invalid
        if check_row() or check_column() or check_sub_grid():
            return True
        return False
