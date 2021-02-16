"""A Sudoku puzzle solver."""

# Standard library imports
import tkinter as tk

# Local imports
from sudoku_solver.classes.controller import Controller


def main() -> None:
    """Initialises fundamental components."""
    root = tk.Tk()
    root.title("Sudoku Solver")
    Controller(root)

    # Enforce minimum size of window
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


if __name__ == "__main__":
    main()
