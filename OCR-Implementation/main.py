import sys

from PySide6.QtWidgets import QApplication
from gui import SudokuGUI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SudokuGUI()
    w.show()
    sys.exit(app.exec())
