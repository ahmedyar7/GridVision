#include <bits/stdc++.h>
using namespace std;

void printBoard(const vector<vector<char>>& board) {
  for (int i = 0; i < 9; i++) {
    for (int j = 0; j < 9; j++) {
      cout << board[i][j] << " ";
    }
    cout << endl;
  }
}

bool isSafe(vector<vector<char>>& board, int row, int col, char digit) {
  // Horizontal checking
  for (int j = 0; j < 9; j++) {
    if (board[row][j] == digit) {
      return false;
    }
  }

  // Vertical checking
  for (int i = 0; i < 9; i++) {
    if (board[i][col] == digit) {
      return false;
    }
  }

  // Grid
  int startingRow = (row / 3) * 3;
  int startingCol = (col / 3) * 3;

  // Check for 3x3 matrix
  for (int i = startingRow; i <= startingRow + 2; i++) {
    for (int j = startingCol; j <= startingCol + 2; j++) {
      if (board[i][j] == digit) {
        return false;
      }
    }
  }

  return true;
}

bool helper(vector<vector<char>>& board, int row, int col) {
  if (row == 9) {
    return true;
  }

  int nextRow = row;
  int nextCol = col + 1;

  if (nextCol == 9) {
    nextRow = row + 1;
    nextCol = 0;
  }

  // Digit already exist
  if (board[row][col] != '.') {
    // Call for the next row and next col;
    return helper(board, nextRow, nextCol);
  }

  //   Placing the correct digit
  for (char digit = '1'; digit <= '9'; digit++) {
    // Is the digit safe to place
    if (isSafe(board, row, col, digit)) {
      board[row][col] = digit;

      if (helper(board, nextRow, nextCol)) {
        return true;
      }

      board[row][col] = '.';
    }
  }

  return false;
}

void solveSudoku(vector<vector<char>>& board) {
  helper(board, 0, 0);
  return;
}

// Solve one test case
void solve() {
  vector<vector<char>> board(9, vector<char>(9));

  for (int i = 0; i < 9; i++) {
    for (int j = 0; j < 9; j++) {
      cin >> board[i][j];
    }
  }

  solveSudoku(board);  // Call your solver

  printBoard(board);
}

int main() { solve(); }