def print_in_box(text):
    border = "+" + "-" * (len(text) + 2) + "+"
    middle = "| " + text + " |"
    print(border)
    print(middle)
    print(border)


def print_sudoku(board, title="Sudoku"):
    print(f"\n{title}:")
    print("+-------+-------+-------+")
    for i, row in enumerate(board):
        print("|", end=" ")
        for j, val in enumerate(row):
            cell = val if val != "." else "."
            print(cell, end=" ")
            if (j + 1) % 3 == 0:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0:
            print("+-------+-------+-------+")
