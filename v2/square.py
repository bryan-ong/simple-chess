from const import *


class Square:
    def __init__(self, row, col, board, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.get_alpha_col(col) # Attributes a letter to column number
        self.board = board # Don't want to refactor all my Square constructors, will default to None

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

    def is_safe(self, color):
        return not self.is_under_attack(color)

    def is_under_attack(self, color):
        enemy_color = "black" if color == "white" else "white"

        for row in range(ROWS):
            for col in range(COLS):
                # if self.has_enemy_piece(): Cannot use has_enemy_piece() here
                piece = self.board.squares[row][col].piece
                if piece and piece.color == enemy_color:
                    piece.clear_moves() # It's best to clear before recalculating
                    self.board.calc_moves(piece, row, col, False)
                    # Now check if this square is in any legal moves of enemy color
                    for move in piece.valid_moves:
                        if move.final.row == self.row and move.final.col == self.col:
                            return True
        return False

    def is_empty_and_not_under_attack(self, color):
        return self.is_empty() and not self.is_under_attack(color)

    def __str__(self):
        return f"""
Square:
Row: {self.row}
Col: {self.col}
Piece: {self.piece}
"""

    @staticmethod # Helper method
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > COLS - 1:
                return False
        return True

    @staticmethod
    def get_alpha_col(col):
        if col < 0:
            return ""
        quotient, remainder = divmod(col, 26)
        return Square.get_alpha_col(quotient - 1) + chr(remainder + ord('A'))
        # Quotient - 1 as we start from 0 in programming
        # If quotient = 0 then we return nothing, so if I were to put 3 in, it would return "D" instead of "AD"
        # The chr part returns the ordinal which is 97 + the remainder of the alphabet in order to get the actual alphabet, of course you could just do + 97 instead of ord
        # From https://www.reddit.com/r/learnprogramming/comments/p7ae0d/comment/h9j05s5/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button


    # Converts numbers to letters excel style (1 = A, 27 = AA)
