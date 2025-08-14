from img_processing import extract_grid
from ocr_utils import extract_board
from solver import solve_with_cpp


def print_in_box(text):
    border = "+" + "-" * (len(text) + 2) + "+"
    middle = "| " + text + " |"
    print(border)
    print(middle)
    print(border)


if __name__ == "__main__":
    img_path = "./imgs/sudoku_face_share1.png"

    # Step 1: Extract Sudoku grid
    warped = extract_grid(img_path)

    # Step 2: OCR digits into a board
    board = extract_board(warped)

    print("Extracted Sudoku Board:")
    for row in board:
        print(row)

    # Step 3: Solve with fast C++ solver
    print_in_box("Solved Sudoku")

    solved = solve_with_cpp(board)
    for row in solved:
        print(row)
