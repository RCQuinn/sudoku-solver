import tkinter as tk


class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Inherit from tkinter
        self.initialise()

    def initialise(self):
        self.configure(bg="black")

        # Grid
        for i in range(9):
            for j in range(9):
                frame = tk.Frame(master=self, relief=tk.RIDGE, borderwidth=1)

                if i == 3 or i == 6:
                    frame.grid(row=i, column=j, sticky="nsew", padx=1, pady=(5, 1))
                elif j == 2 or j == 5:
                    frame.grid(row=i, column=j, sticky="nsew", padx=(1, 5), pady=1)
                else:
                    frame.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

                if (i == 3 and (j == 2 or j == 5)) or (i == 6 and (j == 2 or j == 5)):
                    frame.grid(row=i, column=j, sticky="nsew", padx=(1, 5))

                data = tk.Entry(master=frame, width=3, font="Calibri 32", justify="center")
                data.pack(fill='both', expand=True)
                self.grid_columnconfigure(i, weight=1)
                self.grid_rowconfigure(j, weight=1)

        #myButton = tk.Button(self, text="enter your name", command=self.myClick)
        #myButton.grid(row=10)

    def myClick(self):
        print("Hello")


if __name__ == "__main__":
    app = SudokuApp()
    app.title("Sudoku Solver")

    # Prevent resizing
    #app.resizable(0, 0)

    app.update()
    app.minsize(app.winfo_width(), app.winfo_height())

    app.mainloop()
