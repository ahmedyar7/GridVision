"""utils.py

This module contain function that are commoly used in
the project throughout.

"""

import cv2
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
