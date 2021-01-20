class Model:
    def __init__(self, vc):
        self.vc = vc
        self.solution = None
        self.problem = None

    # Delegates-- Model would call this on internal change
    def puzzleChanged(self):
        self.vc.puzzleChangedDelegate()

    def getSolution(self):
        return self.solution

    def getProblem(self):
        return self.problem

    def solve(self, grid):
        self.problem = [x[:] for x in grid]
        self.solution = self.backtracking(grid, 0, 0)
        self.puzzleChanged()

    def backtracking(self, grid, row_index, col_index):
        """ Backtracking algorithm using recursive calls.
        :param grid: 2D list shaped 9 by 9.
        :param row_index: Current position in the row.
        :param col_index: Current position in the column.
        :return: A completed Sudoku puzzle, or None if the puzzle is un-solvable.
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

    def next_space(self, grid, row_index, col_index):
        """ Get next cell, going to next line if row finishes
        :param grid: 2D list shaped 9 by 9.
        :param row_index: Current position in the row.
        :param col_index: Current position in the column.
        :return: A call to the function that calls this method.
        """
        if col_index == 8:  # If row finishes, go to next line.
            col_index = 0
            return self.backtracking(grid, row_index + 1, col_index)
        else:
            return self.backtracking(grid, row_index, col_index + 1)

    @staticmethod
    def is_invalid(grid, row_index, col_index, value):
        """ Checks for duplicate values based on Sudoku rules.
        :param grid: 2D list shaped 9 by 9.
        :param row_index: Row to check.
        :param col_index: Column to check.
        :param value: Value to check against.
        :return: Boolean True if a duplicate is found, else false.
        """

        def check_row():
            for column in range(9):
                if grid[row_index][column] == value:
                    return True
            return False

        def check_column():
            for row in range(9):
                if grid[row][col_index] == value:
                    return True
            return False

        def check_sub_grid():
            topr = row_index - (row_index % 3)  # Find top corner of grid
            topc = col_index - (col_index % 3)  # for row and column.
            for r in range(topr, topr + 3):
                for c in range(topc, topc + 3):
                    if grid[r][c] == value:
                        return True
            return False

        # If ANY match is found, that value is invalid
        if check_row() or check_column() or check_sub_grid():
            return True
        return False
