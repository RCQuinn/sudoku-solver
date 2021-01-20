# sudoku_solver
# 2021 by Ramen Crowe
#
# A sudoku puzzle solver based on the Model-View-Controller framework.
# Thanks to Steven Lipton for the template:
#   (https://makeapppie.com/2014/05/23/from-apple-to-raspberry-pi-a-mvc-template-for-tkinter/

import tkinter as tk
from classes.controller import Controller


def main():
    root = tk.Tk()
    root.title("Sudoku Solver")
    Controller(root)

    # Enforce minimum size of window
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


if __name__ == "__main__":
    main()
