from classes.model import Model
from classes.view import View


class Controller:
    def __init__(self, root):
        self.root = root
        self.model = Model(self)
        self.view = View(self)

        # Initialize objects in view
        self.view.setLabelText("Ready")

    def quitButtonPressed(self):
        self.root.destroy()

    def puzzleChangedDelegate(self):
        # Model internally changes and needs to signal a change
        solution = self.model.getSolution()
        problem = self.model.getProblem()
        if solution is not None:
            flatten_solution = [i for sub in solution for i in sub]  # Flatten 2D to 1D
            flatten_problem = [i for sub in problem for i in sub]
            self.view.setEntryGrid(flatten_solution, flatten_problem)
            self.view.setLabelText("Solution found!")
        else:
            self.view.setLabelText("Unable to find solution")

    def getSolution(self, entries):
        sudoku_grid = self.convertGrid(entries)

        if self.validate_user_grid(sudoku_grid):
            self.model.solve(sudoku_grid)
        else:
            self.view.setLabelText("Invalid puzzle. Check values again.")

    def clear(self):
        self.view.clearGrid()
        self.view.setLabelText("Ready")

    @staticmethod
    def validateEntry(i, S):
        """ Allow ONLY numbers 1->9 and no longer than 1 character.
        :param i: index of char string to be inserted/deleted, or -1
        :param S: the text string being inserted or deleted, if any
        :return: Boolean true if valid input, else false
        """
        if S in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and int(i) == 0:
            return True
        return False

    @staticmethod
    def convertGrid(entries):
        # Assumes a list that contains only string representations of numbers and empty values.
        entry_length = len(entries)
        if entry_length != 81:
            print("Format is not 9x9 Sudoku. Error.")
            exit()

        values = [entry.get() for entry in entries]  # Get values from the entry.

        # Convert empty values to 0s
        for i in range(entry_length):
            if values[i] == '':
                values[i] = 0
            else:
                values[i] = int(values[i])

        # Convert 1D list to 2D
        return [values[i:i + 9] for i in range(0, entry_length, 9)]

    def validate_user_grid(self, grid):
        # TODO
        # Check duplicates in row
        for value in range(1, 10):      # Check row for duplicates
            for row in range(9):
                if grid[row].count(value) > 1:
                    return False
            for column in range(9):     # Check column for duplicates
                if grid[column].count(value) > 1:
                    return False

            for rc in range(1, 10, 3):  # Check sub grid for duplicates
                for cc in range(1, 10, 3):
                    lst = [grid[rc - 1][cc - 1], grid[rc - 1][cc], grid[rc - 1][cc + 1],
                           grid[rc][cc - 1], grid[rc][cc], grid[rc][cc + 1],
                           grid[rc + 1][cc - 1], grid[rc + 1][cc], grid[rc + 1][cc + 1]
                           ]
                    if lst.count(value) > 1:
                        return False
        return True
