from operator import attrgetter


class SudokoSolver:
    def __init__(self):
        pass

    def check_valid_puzzle(self, arr) -> True:
        """
        Validates whether a given Sudoku puzzle is valid.

        This method checks the validity of a Sudoku grid by verifying the following:
        1. Each row contains unique non-zero digits (1-9) with no repetition.
        2. Each column contains unique non-zero digits (1-9) with no repetition.
        3. Each 3x3 sub-square grid (sub-square) contains unique non-zero digits (1-9) with no repetition.

        Parameters:
        -----------
        arr : list[list[int]]
            A 2D list representing a 9x9 Sudoku grid where each cell contains an integer (0-9).
            A value of '0' indicates an empty cell.

        Returns:
        --------
        bool
            Returns True if the Sudoku grid is valid according to Sudoku rules.
            Returns False if any row, column, or sub-square grid contains duplicate non-zero values.
        """
        sub_squares_starting_point = [
            [0, 0],
            [0, 3],
            [0, 6],
            [3, 0],
            [3, 3],
            [3, 6],
            [6, 0],
            [6, 3],
            [6, 6],
        ]

        # checking for the rows
        for rows in range(9):
            contained = set()
            for cols in range(9):
                if arr[rows][cols] == 0:
                    continue
                if arr[rows][cols] in contained:
                    return False

                contained.add(arr[rows][cols])

        # checking for the columns
        for cols in range(9):
            contained = set()
            for rows in range(9):
                if arr[rows][cols] == 0:
                    continue
                if arr[rows][cols] in contained:
                    return False

                contained.add(arr[rows][cols])

        # Checking for the Sub Square grid
        for point_row, point_col in sub_squares_starting_point:
            contained = set()
            for rows in range(3):
                for cols in range(3):
                    if arr[point_row + rows][point_col + cols] == 0:
                        continue
                    if arr[point_row + rows][point_col + cols] in contained:
                        return False
                    contained.add(arr[point_row + rows][point_col + cols])

        return True

    def print_board(self, arr):

        for i in range(9):
            for j in range(9):
                if arr[i][j] == 0:
                    print("_", end=" ")
                else:
                    print(arr[i][j], end=" ")
                print(end=" ")

    @staticmethod
    def sudoko_solver(arr):
        positions = []

        def add_position(ch, r, c, x):
            positions.append(
                [
                    ch,
                    [
                        9 * r + x,
                        81 + 9 * c + x,
                        162 * 9 * ((r // 3) * 3 + (c // 3)) + x,
                        243 + 9 + r + c,
                    ],
                ]
            )
