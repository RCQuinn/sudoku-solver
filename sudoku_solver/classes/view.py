# PEP 563 -- Postponed Evaluation of Annotations. Avoids circular imports.
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller

# Standard library imports
import tkinter as tk
from typing import List


class View:
    """Container for all the UI elements for a Sudoku grid."""
    def __init__(self, vc: Controller) -> None:
        self.vc = vc
        self.root = vc.root               # type: tk.Tk
        self.label_text = tk.StringVar()  # type: tk.StringVar
        self.puzzle_input = []            # type: List[tk.Entry]

        self.load_view()

    def load_view(self) -> None:
        """Creates and configures the:
            Main window containing everything,
            Main panel containing the grid of Entry objects,
            Side panel containing buttons for functionality,
            Bottom panel containing a text display and quit button.
        """
        # ### Window ###
        self.root.configure(background="white")
        self.root.grid_columnconfigure(0, weight=1)  # Allow resizing of the frame containing
        self.root.grid_rowconfigure(0, weight=1)  # the puzzle ONLY.

        # ### Main panel ###
        puzzle_frame = tk.Frame(master=self.root, borderwidth=1, background="black")
        puzzle_frame.grid(row=0, column=0, sticky="nsew")

        P1 = 1  # Default thin padding between all squares
        P5 = 5  # Thick padding in grid separators
        padding = {
            **dict.fromkeys([(0, 2), (1, 2), (3, 2), (4, 2), (6, 2), (7, 2), (8, 2)], ((P1, P5), (P1, P1))),  # L Column
            **dict.fromkeys([(0, 5), (1, 5), (3, 5), (4, 5), (6, 5), (7, 5), (8, 5)], ((P1, P5), (P1, P1))),  # R Column
            **dict.fromkeys([(2, 0), (2, 1), (2, 3), (2, 4), (2, 6), (2, 7), (2, 8)], ((P1, P1), (P1, P5))),  # Up Row
            **dict.fromkeys([(5, 0), (5, 1), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8)], ((P1, P1), (P1, P5))),  # Low Row
            **dict.fromkeys([(2, 2), (2, 5), (5, 2), (5, 5)], ((P1, P5), (P1, P5))),  # Inner Corners
        }

        for row in range(9):
            for column in range(9):
                puzzle_frame.grid_columnconfigure(column, weight=1)  # Allow user to resize the window so
                puzzle_frame.grid_rowconfigure(row, weight=1)  # that all squares resize evenly.

                # Create a frame for each square of the puzzle
                square = tk.Frame(master=puzzle_frame, height=100, width=100, bg="black", borderwidth=1)

                pair = (row, column)
                if pair in padding:
                    square.grid(row=row, column=column, sticky="nsew", padx=padding[pair][0], pady=padding[pair][1])
                else:
                    square.grid(row=row, column=column, sticky="nsew", padx=P1, pady=P1)

                # i: index of char string to be inserted/deleted, or -1.
                # S : the text string being inserted or deleted, if any.
                validate_cmd = (self.root.register(self.vc.validateEntry), '%i', '%S')
                data = tk.Entry(master=square, width=3, font=("Calibri", 32), justify="center", validate="key",
                                validatecommand=validate_cmd)
                data.pack(fill='both', expand=True)

                self.puzzle_input.append(data)

        # ### Side panel ###
        side_frame = tk.Frame(self.root, borderwidth=1, background="white")
        side_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        button_frame = tk.Frame(master=side_frame, bg='white')
        button_frame.pack(side="left", ipady=10)
        tk.Button(master=button_frame, text="SOLVE", height=5, width=10,
                  command=lambda: self.vc.send_data(self.puzzle_input)).pack(side="top")
        tk.Button(master=button_frame, text="CLEAR", height=5, width=10,
                  command=lambda: self.vc.clear()).pack(side="bottom")

        # ### Bottom Panel ###
        tk.Label(self.root, textvariable=self.label_text, bg="white").grid(row=1, column=0, sticky="ew")
        tk.Button(self.root, text='Quit',
                  command=lambda: self.vc.quit_button_pressed()).grid(row=1, column=1, sticky="ew")

    def set_label_text(self, text: str) -> None:
        """Changes text display."""
        self.label_text.set(text)

    def set_entry_grid(self, solution: List[int], problem: List[int]) -> None:
        """Fills out the grid display with new values, setting existing values to bold."""
        for i in range(len(solution)):
            entry = self.puzzle_input[i]

            if solution[i] != problem[i]:
                entry.delete(0, tk.END)
                entry.insert(0, solution[i])
            else:
                entry.configure(font=("Calibri", 32, 'bold'))

    def clear_grid(self) -> None:
        """Removes values from grid display."""
        for i in range(len(self.puzzle_input)):
            entry = self.puzzle_input[i]
            entry.delete(0, tk.END)
            entry.configure(font=("Calibri", 32))
