import os
import sys
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from img_processing import extract_grid
from ocr_utils import extract_board
from solver import solve_with_cpp
from utils import print_sudoku, draw_sudoku_image


class SudokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Sudoku Solver")
        self.setMinimumSize(900, 600)

        self.image_path = None
        self.output_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

        # Widgets
        self.open_btn = QPushButton("1) Open Image")
        self.solve_btn = QPushButton("2) Solve & Save Image")
        self.solve_btn.setEnabled(False)

        self.orig_label = QLabel("Original")
        self.orig_label.setAlignment(Qt.AlignCenter)
        self.orig_label.setStyleSheet("border: 1px solid #aaa;")
        self.orig_label.setMinimumSize(400, 400)
        self.orig_label.setScaledContents(True)

        self.result_label = QLabel("Solved Image Preview")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("border: 1px solid #aaa;")
        self.result_label.setMinimumSize(400, 400)
        self.result_label.setScaledContents(True)

        # Layouts
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.open_btn)
        btn_row.addWidget(self.solve_btn)

        img_row = QHBoxLayout()
        img_row.addWidget(self.orig_label)
        img_row.addWidget(self.result_label)

        root = QVBoxLayout()
        root.addLayout(btn_row)
        root.addLayout(img_row)
        self.setLayout(root)

        # Signals
        self.open_btn.clicked.connect(self.open_image)
        self.solve_btn.clicked.connect(self.run_pipeline)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Sudoku Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
        )
        if not file_name:
            return

        self.image_path = file_name
        self.orig_label.setPixmap(QPixmap(file_name))
        self.result_label.setText("Solved Image Preview")
        self.solve_btn.setEnabled(True)

    def run_pipeline(self):
        if not self.image_path:
            QMessageBox.warning(self, "No Image", "Please open a Sudoku image first.")
            return

        try:
            # : Extract Sudoku grid (warped)
            warped = extract_grid(self.image_path)

            # OCR digits to board (0 for blanks)
            board = extract_board(warped)
            print_sudoku(board, "Extracted Sudoku Board")

            #  Solve with C++ exe
            solved = solve_with_cpp(board)
            print_sudoku(solved, "Solved Sudoku Board")

            # Step 4: Create solved Sudoku image
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_clean = os.path.join(self.output_dir, f"solved_board_{stamp}.png")
            draw_sudoku_image(solved, out_clean)

            #  show solved image in GUI
            self.result_label.setPixmap(QPixmap(out_clean))

            QMessageBox.information(
                self, "Done", f"Solved Sudoku image saved:\n{out_clean}"
            )

        except FileNotFoundError as e:
            # Common case: solver .exe path issue
            QMessageBox.critical(
                self,
                "Executable not found",
                f"{e}\n\nTip: resolve the solver.exe path using __file__ in solver.py.",
            )
        except AssertionError as e:
            QMessageBox.critical(self, "Board Error", f"{e}")
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SudokuGUI()
    w.show()
    sys.exit(app.exec())
