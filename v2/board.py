import copy
import math
import sys

import v2.game
from square import Square
from piece import *
from const import *
from move import Move
from soundmanager import SoundManager


class Board:
    def __init__(self, player_count):
        self.checkmated = False
        self.squares = [[Square(row, col, self, self) for col in range(COLS)] for row in range(ROWS)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.last_move = None
        self.pending_promotion = False
        self.promote_option = None
        self.player_count = player_count
        self._move_cache = {}  # Caching
        self.was_last_move_capture = False
        self.winner = None

    def in_check(self, color):
        # Checks if the king is in check for that color
        king_pos = None
        # Find the king's position
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos: # If no king, game is probably over
            return False

        # Check if any enemy piece can attack the king
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color != color:
                    # Use cached moves if available
                    cache_key = (piece.__class__.__name__, row, col, color)
                    if cache_key not in self._move_cache:
                        self.calc_moves(piece, row, col, check_check=False) # Calculate all the valid moves and sets valid_moves[] to the result
                        self._move_cache[cache_key] = piece.valid_moves

                    for move in self._move_cache[cache_key]:
                        if move.final.row == king_pos[0] and move.final.col == king_pos[1]: # Check if king in list of valid moves
                            return True
        return False

    def calc_moves(self, piece, row, col, check_check=True):
        # Calculate all valid moves for a piece at given position
        piece.clear_moves()

        # First get all pseudo-legal moves ( moves that each piece can take, not accounting for checks )
        self.calc_pseudo_legal_moves(piece, row, col)

        if not check_check: # If the king is not in check, just cancel as there is no need to filter out legal moves
            return

        valid_moves = []
        for move in piece.valid_moves:
            if not self._move_leaves_king_in_check(piece, row, col, move): # Method name says it all
                valid_moves.append(move)

        piece.valid_moves = valid_moves


    def _move_leaves_king_in_check(self, piece, row, col, move):
        # Save original state
        original_piece = self.squares[move.final.row][move.final.col].piece
        original_moved = piece.moved

        # Make the move temporarily
        self.squares[row][col].piece = None
        self.squares[move.final.row][move.final.col].piece = piece
        piece.moved = True

        # Find the king's position
        king_pos = None
        for r in range(ROWS):
            for c in range(COLS):
                sq_piece = self.squares[r][c].piece
                if isinstance(sq_piece, King) and sq_piece.color == piece.color:
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        in_check = False
        if king_pos:
            # Check if any enemy piece can attack the king
            for r in range(ROWS):
                for c in range(COLS):
                    enemy_piece = self.squares[r][c].piece
                    if enemy_piece and enemy_piece.color != piece.color:
                        enemy_piece.clear_moves()
                        self.calc_pseudo_legal_moves(enemy_piece, r, c)
                        for enemy_move in enemy_piece.valid_moves:
                            if (enemy_move.final.row == king_pos[0] and
                                    enemy_move.final.col == king_pos[1]):
                                in_check = True
                                break
                        if in_check:
                            break

        # Reverts to the original move
        self.squares[row][col].piece = piece
        self.squares[move.final.row][move.final.col].piece = original_piece
        piece.moved = original_moved

        return in_check

    def calc_pseudo_legal_moves(self, piece, row, col):
        # Calculate all moves for selected piece, pseudo legal as we have yet to account for checks / pins
        if isinstance(piece, Pawn):
            self._calc_pawn_moves(piece, row, col)
        elif isinstance(piece, Knight):
            self._calc_knight_moves(piece, row, col)
        elif isinstance(piece, Bishop):
            self._calc_bishop_moves(piece, row, col)
        elif isinstance(piece, Rook):
            self._calc_rook_moves(piece, row, col)
        elif isinstance(piece, Queen):
            self._calc_queen_moves(piece, row, col)
        elif isinstance(piece, King):
            self._calc_king_moves(piece, row, col)

    def _calc_pawn_moves(self, piece, row, col):
        # Gets all pawn moves
        # Safer to create temporary moves[] and set the instance variable to the temporary moves[] as I was encountering some bugs like being able to capture the pawn in front not diagonal
        moves = []
        direction = piece.dir
        start_row = 1 if piece.color == "black" else ROWS - 2
        # Forward moves
        if Square.in_range(row + direction) and self.squares[row + direction][col].is_empty(): # If square in front of pawn is empty, append the move
            moves.append(Move(Square(row, col, self), Square(row + direction, col, self)))
            if row == start_row and Square.in_range(row + 2 * direction) and self.squares[row + 2 * direction][col].is_empty():
                # Same as above but for 2 squares ahead, for loop could be used but since only 2 statements needed it is fine
                moves.append(Move(Square(row, col, self), Square(row + 2 * direction, col, self)))

        # Captures
        for dc in [-1, 1]:
            if Square.in_range(row + direction, col + dc):
                target = self.squares[row + direction][col + dc]
                if target.has_enemy_piece(piece.color):
                    moves.append(Move(Square(row, col, self), Square(row + direction, col + dc, self, target.piece)))

        # En passant
        if self.last_move:
            final = self.last_move.final

            if isinstance(self.squares[final.row][final.col].piece, Pawn):
                prev_pawn = self.squares[final.row][final.col].piece
                if abs(self.last_move.initial.row - self.last_move.final.row) == 2: # Check if the last move was a pawn and if it has moved 2 squares
                    if row == self.last_move.final.row and abs(col - self.last_move.final.col) == 1:
                        moves.append(Move(Square(row, col, self), Square(row + direction, self.last_move.final.col, self), captured_piece=prev_pawn))

        piece.valid_moves = moves

    def _calc_knight_moves(self, piece, row, col):

        moves = []
        possible_moves = [
            (row - 2, col + 1), (row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1),
            (row + 2, col - 1), (row + 1, col - 2), (row - 1, col - 2), (row - 2, col - 1)
        ]
        # r c stand for row and col since they are already used as params
        for r, c in possible_moves:
            if Square.in_range(r, c) and self.squares[r][c].is_empty_or_enemy(piece.color):
                moves.append(Move(Square(row, col, self), Square(r, c, self, self.squares[r][c].piece)))

        piece.valid_moves = moves

    def _calc_sliding_moves(self, piece, row, col, directions):
        # General method for sliding/straightline pieces
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while Square.in_range(r, c):
                target = self.squares[r][c]
                if target.is_empty():
                    moves.append(Move(Square(row, col, self), Square(r, c, self)))
                elif target.has_enemy_piece(piece.color):
                    moves.append(Move(Square(row, col, self), Square(r, c, self, target.piece)))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

    def _calc_bishop_moves(self, piece, row, col):
        piece.valid_moves = self._calc_sliding_moves(piece, row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def _calc_rook_moves(self, piece, row, col):
        piece.valid_moves = self._calc_sliding_moves(piece, row, col, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def _calc_queen_moves(self, piece, row, col):
        piece.valid_moves = self._calc_sliding_moves(piece, row, col,
                                                     [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
                                                      (1, 1)])

    def _calc_king_moves(self, piece, row, col):
        moves = []
        # Normal moves, the adjacent ones
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if Square.in_range(r, c) and self.squares[r][c].is_empty_or_enemy(piece.color):
                    moves.append(Move(Square(row, col, self), Square(r, c, self, self.squares[r][c].piece)))

        # Castling
        if not piece.moved:
            king_side = Move(Square(row, col, self), Square(row, col + 2, self))
            queen_side = Move(Square(row, col, self), Square(row, col - 2, self))
            # King side
            # Checks if the 6th and 7th column is empty ( will add a method to combine both empty and attacked checks )

            if self.can_castle(piece, row, col, kingside=True):
                moves.append(king_side)
                    # This is not working. I'll try just making separate methods for these

            elif self.can_castle(piece, row, col, kingside=False):
                moves.append(queen_side)





        piece.valid_moves = moves

    def can_castle(self, piece, row, col, kingside=True):

        if kingside:
            if (self.squares[row][col + 1].is_empty_and_not_under_attack(piece.color)
            and self.squares[row][col + 2].is_empty_and_not_under_attack(piece.color)):
                if isinstance(self.squares[row][col + 3].piece, Rook) and not self.squares[row][col + 3].piece.moved:  # Check if the rook on the last column has moved
                    return True
            return False
        else: # I would use a for loop but right now trying to debug
            if (self.squares[row][1].is_empty_and_not_under_attack(piece.color)
            and self.squares[row][2].is_empty_and_not_under_attack(piece.color)
            and self.squares[row][3].is_empty_and_not_under_attack(piece.color)):

                if isinstance(self.squares[row][0].piece, Rook) and not self.squares[row][0].piece.moved:  # Check if the rook on the last column has moved
                    return True
            return False

    def is_checkmate(self, color):
        # This checks if a color is checked for the current game state
        if not self.in_check(color):
            return False

        # Check if any piece has any valid move
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col)
                    if piece.valid_moves:
                        return False
        return True

    def move(self, piece, move, testing=False):
        if not testing and not self.valid_move(piece, move):
            return False

        initial = move.initial
        final = move.final

        # Clear cache
        self._move_cache = {}

        # Execute the move
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Handle special moves
        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            # print(diff)
            # print(self.squares[final.row][final.col])
            if diff != 0:
                # print("2")
                self.squares[initial.row][final.col].piece = None
                if not testing:
                    # print("3")
                    self.was_last_move_capture = True

        elif isinstance(piece, King):
            # Castling
            if abs(initial.col - final.col) == 2 and not testing:
                # Kingside
                (row, col) = initial.row, initial.col
                if final.col > initial.col: # Means move to the right
                    rook = self.squares[initial.row][col + 3].piece
                    self.squares[row][col + 3].piece = None
                    self.squares[row][col + 2].piece = piece
                    self.squares[row][col + 1].piece = rook
                # Queenside
                else:
                    rook = self.squares[row][col - 4].piece
                    self.squares[row][col - 4].piece = None
                    self.squares[row][col - 2].piece = piece
                    self.squares[row][col - 1].piece = rook
                SoundManager().play("castle")
        piece.moved = True
        self.last_move = move

        # Check for check/checkmate
        if not testing:
            opponent_color = "black" if piece.color == "white" else "white"
            if self.is_checkmate(opponent_color):
                SoundManager().play("checkmate")
                self.checkmated = True
                self.winner = piece.color
            elif self.in_check(opponent_color):
                SoundManager().play("check")
            elif self.was_last_move_capture:
                SoundManager().play("capture")
            else:
                SoundManager().play("move")

        return True

    def valid_move(self, piece, move):
        return move in piece.valid_moves

    def check_promote(self, piece, final):
        if isinstance(piece, Pawn):
            if final.row == 0 or final.row == ROWS - 1:
                piece.should_promote = True
                self.pending_promotion = True

    def set_promote_piece(self, piece, final, option):
        self.squares[final.row][final.col].piece = option(piece.color)
        piece.should_promote = False
        self.pending_promotion = False



    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col, self)

    def _add_pieces(self, color):
        row_pawn, row_other = (COLS - 2, COLS - 1) if color == "white" else (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, self, Pawn(color))

        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(COLS):
            # Get the piece class using modulo to cycle through the list, in case there are more than 8x8
            piece_class = pieces[col % len(pieces)]
            self.squares[row_other][col] = Square(row_other, col, self, piece_class(color))