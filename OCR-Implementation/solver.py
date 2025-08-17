import subprocess


def solve_with_cpp(board):
    # Convert Python board (list of lists of ints) to string format for C++
    input_str = "\n".join(
        [" ".join(str(c) if c != 0 else "." for c in row) for row in board]
    )

    # Run the C++ solver
    # For linux and macOS use .out instead of .exe

    result = subprocess.run(
        ["../Helper/sudoko_solver.exe"],  # use "sudoku_solver.exe" on Windows
        input=input_str,
        text=True,
        capture_output=True,
    )

    output_lines = result.stdout.strip().split("\n")
    solved_board = [[int(c) for c in line.split()] for line in output_lines]
    return solved_board
