from mypy import api


def type_check_program():
    result = api.run(["../sudoku_solver"])
    if result[0]:
        print('\nType checking report:\n')
        print(result[0])  # stdout
    if result[1]:
        print('\nError report:\n')
        print(result[1])  # stderr
    print('\nExit status:', result[2])
