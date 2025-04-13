from const import *


class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.get_alpha_col(col) # Attributes a letter to column number

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return not self.has_piece()

    def has_enemy_piece(self, color):
        # Check if square has piece and the piece is not that of the given color
        return self.has_piece() and self.piece.color != color

    def has_ally_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def is_empty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy_piece(color)

    @staticmethod # Helper method
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > COLS - 1:
                return False
        return True

    @staticmethod
    def get_alpha_col(col):
        return "" if col < 0 else Square.get_alpha_col(col // 26 - 1) + chr(col % 26 + ord("A"))
    # From https://www.reddit.com/r/learnprogramming/comments/p7ae0d/comment/h9j05s5/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

    # Converts numbers to letters excel style (1 = A, 27 = AA)
