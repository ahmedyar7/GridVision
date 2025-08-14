import cv2
import numpy as np


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


def extract_grid(img_path, side=450):
    """Load and warp Sudoku grid from an image"""
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(
        img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contour = max(contours, key=cv2.contourArea)

    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    points = reorder(approx)

    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [side, 0], [side, side], [0, side]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(img, matrix, (side, side))

    return warped
