"""utils.py

This module contain function that are commoly used in
the project throughout.

"""

import cv2


def image_processing_and_thresholding(img):
    """
    This is the utility function that would take the img_path
    and peform some img processing using opencv and then return the
    threshold of the image
    """

    # Image Processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # Thresholding
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    return thresh


def print_in_box(text):
    border = "+" + "-" * (len(text) + 2) + "+"
    middle = "| " + text + " |"
    print(border)
    print(middle)
    print(border)


def print_sudoku(board, title="Sudoku"):
    print(f"\n{title}:")
    print("+-------+-------+-------+")
    for i, row in enumerate(board):
        print("|", end=" ")
        for j, val in enumerate(row):
            cell = val if val != "." else "."
            print(cell, end=" ")
            if (j + 1) % 3 == 0:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0:
            print("+-------+-------+-------+")
