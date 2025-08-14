from img_processing import extract_grid
from ocr_utils import extract_board
from solver import solve_with_cpp
from utils import print_in_box, print_sudoku


if __name__ == "__main__":
    img_path = "./imgs/sudoku_face_share1.png"

    # Step 1: Extract Sudoku grid
    warped = extract_grid(img_path)

    # Step 2: OCR digits into a board
    board = extract_board(warped)

    # Print unsolved board
    print_sudoku(board, "Extracted Sudoku Board")

    # Step 3: Solve with fast C++ solver
    solved = solve_with_cpp(board)

    # print_in_box("Solved Sudoku")
    print_sudoku(solved, "Solved Sudoku Board")
