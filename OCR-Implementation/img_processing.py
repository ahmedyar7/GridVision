"""
This module is responsible for reordering the image
 and extracting the grid for easyocr for character recognition
"""

import cv2
import numpy as np


def reorder(points):
    """
    The function reorder takes four points (usually from a contour of a square)
    and returns them in a consistent order:
      - top-left
      - top-right,
      - bottom-right,
      - bottom-left.
    """
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
    """
    This function is responsible for extracting of the
    grid from the image for the easy processing of the
    grid in the EasyOCR(Optical Character Recognition)
    """

    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Image Thresholding for sudoku
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Finding contours for the image
    contours, _ = cv2.findContours(
        img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contour = max(contours, key=cv2.contourArea)

    peri = cv2.arcLength(contour, True)  # frame for the sukoku

    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    points = reorder(approx)

    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [side, 0], [side, side], [0, side]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(img, matrix, (side, side))

    return warped
