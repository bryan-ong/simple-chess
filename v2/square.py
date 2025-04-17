from const import *
from piece import *

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

        # Check pawn attacks
        pawn_dir = 1 if enemy_color == "white" else -1
        for delta_col in [-1, 1]:
            r, delta_col = self.row - pawn_dir, self.col + delta_col
            if Square.in_range(r, delta_col):
                piece = self.board.squares[r][delta_col].piece
                if isinstance(piece, Pawn) and piece.color == enemy_color:
                    return True

        # Check knight attacks
        knight_moves = [
            (self.row - 2, self.col + 1), (self.row - 1, self.col + 2),
            (self.row + 1, self.col + 2), (self.row + 2, self.col + 1),
            (self.row + 2, self.col - 1), (self.row + 1, self.col - 2),
            (self.row - 1, self.col - 2), (self.row - 2, self.col - 1)
        ]
        for r, c in knight_moves:
            if Square.in_range(r, c):
                piece = self.board.squares[r][c].piece
                if isinstance(piece, Knight) and piece.color == enemy_color:
                    return True

        # Check sliding pieces (bishop, rook, queen)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while Square.in_range(r, c):
                piece = self.board.squares[r][c].piece
                if piece:
                    if piece.color == enemy_color:
                        if (abs(dr) == abs(dc) and (isinstance(piece, Bishop) or isinstance(piece, Queen)) or
                                (dr == 0 or dc == 0) and (isinstance(piece, Rook) or isinstance(piece, Queen))):
                                    return True
                    break  # Stop if we hit any piece
                r += dr
                c += dc

        # Check king attacks (adjacent squares)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = self.row + dr, self.col + dc
                if Square.in_range(r, c):
                    piece = self.board.squares[r][c].piece
                    if isinstance(piece, King) and piece.color == enemy_color:
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
