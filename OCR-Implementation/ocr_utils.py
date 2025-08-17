"""ocr_utils.py

This module is responsible for
    1. Extracting the digits from the Image using EasyOCr
    2. Extracting the actual board in form 2d array
"""

import easyocr
import cv2

# Init OCR reader globally (loads only once)
reader = easyocr.Reader(["en"])


def extract_digit(original_img: str):
    """Extract a digit from a single Sudoku cell using EasyOCR."""

    gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    result = reader.readtext(thresh, detail=0, paragraph=False)

    if len(result) > 0:
        text = result[0]
        if text.isdigit():
            return int(text)

    return 0


def extract_board(warped):
    """Extract full Sudoku board as a 2D list of digits (0 = empty)"""
    board = []

    cell_h = warped.shape[0] // 9
    cell_w = warped.shape[1] // 9

    for i in range(9):
        row = []

        for j in range(9):
            y1, y2 = i * cell_h, (i + 1) * cell_h
            x1, x2 = j * cell_w, (j + 1) * cell_w
            cell = warped[y1:y2, x1:x2]

            digit = extract_digit(cell)
            row.append(digit)

        board.append(row)

    return board
