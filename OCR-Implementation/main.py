from img_processing import print_in_box, solve_with_cpp, board

if __name__ == "__main__":
    print_in_box("Extracted Sudoku Board:")
    for row in board:
        print(row)

    # Boxed output
    print("\n")
    print_in_box("Solved Sudoku")

    solved = solve_with_cpp(board)
    for row in solved:
        print(row)
