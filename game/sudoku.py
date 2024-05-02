import random

from game.constants import DIFFICULT


class Sudoku:
    def __init__(self,difficult):
        self.board = [[0] * 9 for _ in range(9)]
        self._difficult = DIFFICULT.get(difficult)

    def generate(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0

        for _ in range(self._difficult):  # Adjust the number of iterations for difficulty
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            while not self.is_valid(row, col, num):
                row, col = random.randint(0, 8), random.randint(0, 8)
                num = random.randint(1, 9)
            self.board[row][col] = num

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    def display(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                print(self.board[i][j] if self.board[i][j] != 0 else '.', end=" ")
            print()

    def is_full(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def make_move(self, row, col, num):
        if self.is_valid(row, col, num):
            self.board[row][col] = num
            return True
        return False
