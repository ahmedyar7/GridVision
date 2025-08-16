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
from utils import print_sudoku

# === Pillow to render the solved Sudoku into an image ===
from PIL import Image, ImageDraw, ImageFont


def draw_sudoku_image(board, output_file="solved_sudoku.png", cell_size=70, margin=20):
    """
    Create a clean solved Sudoku image from a 9x9 board using Pillow.
    board: 9x9 list of ints (1..9)
    """
    assert len(board) == 9 and all(len(row) == 9 for row in board), "board must be 9x9"

    grid_size = cell_size * 9
    W = H = grid_size + margin * 2

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Try a nice readable font; fall back to default
    font = None
    for candidate in ["arial.ttf", "DejaVuSans.ttf"]:
        try:
            font = ImageFont.truetype(candidate, int(cell_size * 0.6))
            break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()

    # Draw grid
    # Outer border
    draw.rectangle([margin, margin, W - margin, H - margin], outline="black", width=3)

    # Internal lines
    for i in range(1, 9):
        x0 = margin + i * cell_size
        y0 = margin + i * cell_size
        # Thicker every 3 cells
        width = 3 if i % 3 == 0 else 1
        # Vertical
        draw.line([(x0, margin), (x0, H - margin)], fill="black", width=width)
        # Horizontal
        draw.line([(margin, y0), (W - margin, y0)], fill="black", width=width)

    # Put digits
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == 0:
                continue
            text = str(val)

            # Center text in cell
            cx = margin + c * cell_size + cell_size / 2
            cy = margin + r * cell_size + cell_size / 2

            # Pillow >=10: textbbox; else fallback to textlength/approx
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            except Exception:
                tw = draw.textlength(text, font=font)
                th = int(cell_size * 0.6)

            draw.text((cx - tw / 2, cy - th / 2), text, fill="black", font=font)

    img.save(output_file)
    return output_file


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
