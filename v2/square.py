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
        # I have to recheck manually instead of using calc_moves as that would call calc_pseudo_legal_moves which will call _king_moves which will call is_under_attack
        # This results in an infinite recursion
        # Also for checking the specific square we can use the position of the square as the root and check from there, however this is hard coded and it is not possible to
        # easily add new piece types

        # Check pawn
        direction = 1 if enemy_color == "white" else -1
        for delta_col in [-1, 1]:
            row, delta_col = self.row - direction, self.col + delta_col
            if Square.on_board(row, delta_col):
                piece = self.board.squares[row][delta_col].piece
                if isinstance(piece, Pawn) and piece.color == enemy_color:
                    return True

        # Check knight
        knight_moves = [
            (self.row - 2, self.col + 1), (self.row - 1, self.col + 2),
            (self.row + 1, self.col + 2), (self.row + 2, self.col + 1),
            (self.row + 2, self.col - 1), (self.row + 1, self.col - 2),
            (self.row - 1, self.col - 2), (self.row - 2, self.col - 1)
        ]
        for row, delta_col in knight_moves:
            if Square.on_board(row, delta_col):
                piece = self.board.squares[row][delta_col].piece
                if isinstance(piece, Knight) and piece.color == enemy_color:
                    return True

        # Check sliding
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for delta_row, delta_col in directions:
            row, col = self.row + delta_row, self.col + delta_col
            while Square.on_board(row, col):
                piece = self.board.squares[row][col].piece
                if piece:
                    if piece.color == enemy_color:
                        if (abs(delta_row) == abs(delta_col) and (isinstance(piece, Bishop) or isinstance(piece, Queen)) or
                                (delta_row == 0 or delta_col == 0) and (isinstance(piece, Rook) or isinstance(piece, Queen))):
                                    return True
                    break  # Stop if we hit any piece
                row += delta_row
                col += delta_col

        # Check king attacks
        for delta_row in [-1, 0, 1]:
            for delta_col in [-1, 0, 1]:
                if delta_row == 0 and delta_col == 0:
                    continue
                row, col = self.row + delta_row, self.col + delta_col
                if Square.on_board(row, col):
                    piece = self.board.squares[row][col].piece
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
    def on_board(*args):
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
