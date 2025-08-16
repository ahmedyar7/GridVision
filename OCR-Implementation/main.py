from img_processing import extract_grid
from ocr_utils import extract_board
from solver import solve_with_cpp
from utils import print_sudoku
from image_viewer import ImageViewer
import sys
from PySide6.QtWidgets import QApplication



if __name__ == "__main__":
    app = QApplication(sys.argv)

    image_viewer = ImageViewer()
    image_viewer.show()

    # ---- Now wait for GUI interaction ----
    app.exec()

    # ---- After window closes ----
    if image_viewer.image_path:
        img_path = image_viewer.image_path
        print(f"Image Path: {img_path}")

        # Step 1: Extract Sudoku grid
        warped = extract_grid(img_path)

        # Step 2: OCR digits into a board
        board = extract_board(warped)

        # Print unsolved board
        print_sudoku(board, "Extracted Sudoku Board")

        # Step 3: Solve with fast C++ solver
        solved = solve_with_cpp(board)
        print_sudoku(solved, "Solved Sudoku Board")
    else:
        print("No image was selected!")