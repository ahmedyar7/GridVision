import subprocess


def solve_with_cpp(board):
    # Convert Python board (list of lists of ints) to string format for C++
    input_str = "\n".join(
        [" ".join(str(c) if c != 0 else "." for c in row) for row in board]
    )

    # Run the C++ solver
    result = subprocess.run(
        ["./Helper/sudoko_solver.exe"],  # use "sudoku_solver.exe" on Windows
        input=input_str,
        text=True,
        capture_output=True,
    )

    # Parse the output back into Python 2D list
    output_lines = result.stdout.strip().split("\n")
    solved_board = [[int(c) for c in line.split()] for line in output_lines]
    return solved_board


# # Example
# board = [
#     [4, 5, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 2, 0, 7, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 2, 8],
#     [0, 0, 0, 0, 5, 0, 0, 0, 0],
#     [0, 8, 0, 0, 0, 0, 2, 0, 0],
#     [0, 2, 0, 0, 0, 0, 0, 5, 0],
#     [0, 1, 0, 0, 0, 0, 4, 0, 0],
#     [0, 0, 0, 0, 4, 5, 0, 0, 0],
#     [0, 0, 8, 0, 0, 0, 0, 0, 0],
# ]

# solved = solve_with_cpp(board)
# for row in solved:
#     print(row)
