import cv2
import numpy as np
import easyocr
from solver import solve_with_cpp

img_path = "./imgs/620sodukujan2013.jpg"

# Load image
img = cv2.imread(img_path)

# PreProcessing
img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_thresh = cv2.adaptiveThreshold(
    img_grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
)

# Grid Detection
contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = max(contours, key=cv2.contourArea)

# Approximating the corners
peri = cv2.arcLength(contour, True)
approx = cv2.approxPolyDP(contour, 0.02 * peri, True)


# Reorder the points: top-left, top-right, bottom-right, bottom-left
def reorder(points):
    points = points.reshape((4, 2))
    new_points = np.zeros((4, 2), dtype=np.float32)

    add = points.sum(1)
    new_points[0] = points[np.argmin(add)]  # top-left
    new_points[2] = points[np.argmax(add)]  # bottom-right

    diff = np.diff(points, axis=1)
    new_points[1] = points[np.argmin(diff)]  # top-right
    new_points[3] = points[np.argmax(diff)]  # bottom-left

    return new_points


points = reorder(approx)

# Warp to get straight sudoku grid
side = 450
pts1 = np.float32(points)
pts2 = np.float32([[0, 0], [side, 0], [side, side], [0, side]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
warped = cv2.warpPerspective(img, matrix, (side, side))

# Debug view
# cv2.imshow("Warped Grid", warped)
# cv2.imshow("Threshold", img_thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# Load EasyOCR reader
reader = easyocr.Reader(["en"])


def extract_digit(cell_img):
    """
    Extract a digit from a single Sudoku cell using EasyOCR.
    Returns digit (int) if found, otherwise 0 for empty cell.
    """
    # Preprocess cell
    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # OCR
    result = reader.readtext(thresh, detail=0, paragraph=False)

    if len(result) > 0:
        text = result[0]
        if text.isdigit():  # keep only digits
            return int(text)
    return 0  # Empty cell


# Extract Sudoku board
board = []
cell_h = warped.shape[0] // 9
cell_w = warped.shape[1] // 9

for i in range(9):
    row = []
    for j in range(9):
        # Extract cell
        y1, y2 = i * cell_h, (i + 1) * cell_h
        x1, x2 = j * cell_w, (j + 1) * cell_w
        cell = warped[y1:y2, x1:x2]

        digit = extract_digit(cell)
        row.append(digit)
    board.append(row)


# print(sudoku_board)

if __name__ == "__main__":

    print("Extracted Sudoku Board:")

    print(type(board))
    for row in board:
        print(row)

    print("\nSolved Sudoko")
    solve_with_cpp(board)

    solved = solve_with_cpp(board)
    for row in solved:
        print(row)
