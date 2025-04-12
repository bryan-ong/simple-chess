import copy

from square import Square
from game import *
from piece import *
from const import *
from move import Move
from soundmanager import SoundManager

class Board:
    def __init__(self):
        # Added 2 list comprehensions so that I can make dynamic sized boards in the future, not sure how useful it would be
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.last_move = None
        self.pending_promotion = False
        self.promote_option = None

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.valid_moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def calc_moves(self, piece, row, col, bool=True):
        # Calculate all the possible (valid) moves of a specific piece in a specific pos

        def get_possible_moves(possible_moves):
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        # Create squares for move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        # Create new move
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break # Add only the protecting move, so break the for loop and don't add any more
                        else:
                            piece.add_move(move)

        def pawn_moves():
            direction = piece.dir  # 1 for white (down), -1 for black (up)
            valid_moves = []

            max_steps = 2 if not piece.moved else 1

            for possible_move_row in range(1, max_steps + 1):
                if Square.in_range(possible_move_row):
                    final_row = row + (direction * possible_move_row)

                    # Check if still on board
                    if not 0 <= final_row < ROWS:
                        break

                    # Check if square is empty
                    if self.squares[final_row][col].is_empty():
                        initial, final = Square(row, col), Square(final_row, col)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                valid_moves.append(move)
                        else:
                            valid_moves.append(move)
                    else:
                        break  # Blocked by piece
                else:
                    break


            # Diagonal captures
            possible_move_rows = [row + direction]
            possible_move_cols = [col - 1, col + 1]

            for possible_move_row in possible_move_rows:
                for possible_move_col in possible_move_cols:
                    # Check if on board
                    if Square.in_range(possible_move_row, possible_move_col):
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            initial, final = Square(row, col), Square(possible_move_row, possible_move_col, final_piece)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move):
                                    valid_moves.append(move)
                            else:
                                valid_moves.append(move)

            # En passant moves
            r = 3 if piece.color == "white" else ROWS - 4
            final_r = 2 if piece.color == "white" else 5
            if row == r:
                # Left
                if Square.in_range(col-1):
                    if self.squares[row][col-1].has_enemy_piece(piece.color):
                        left_pawn = self.squares[row][col-1].piece
                        if isinstance(left_pawn, Pawn):
                            if left_pawn.en_passant:
                                # print("left can passant")
                                initial, final = Square(row, col), Square(final_r, col-1, left_pawn)
                                move = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, move):
                                        valid_moves.append(move)
                                else:
                                    valid_moves.append(move)
                # Right
                if Square.in_range(col+1):
                    if self.squares[row][col + 1].has_enemy_piece(piece.color):
                        right_pawn = self.squares[row][col + 1].piece
                        if isinstance(right_pawn, Pawn):
                            # print("right ", right_pawn.en_passant)
                            if right_pawn.en_passant:
                                initial, final = Square(row, col), Square(final_r, col + 1, right_pawn)
                                move = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, move):
                                        valid_moves.append(move)
                                else:
                                    valid_moves.append(move)


            # For some reason we need to create a new valid moves[] and then set the piece's valid moves to this, as appending directly to the piece doesn't seem to work
            piece.valid_moves = valid_moves

        def knight_moves():
            possible_moves = [  # Coded in a way that y is determined before x
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            get_possible_moves(possible_moves)

        def straight_line_moves(increments):  # Increments
            for increment in increments:
                row_inc, col_inc = increment
                possible_move_row = row + row_inc
                possible_move_col = col + col_inc

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        target_square = self.squares[possible_move_row][possible_move_col]
                        if target_square.is_empty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)


                        # Continue checking (not really needed but should add for resiliency anyways)
                        elif target_square.has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                                else:
                                    break  # Add only the protecting move, so break the for loop and don't add any more
                            else:
                                piece.add_move(move)
                            break  # Stop checking

                        elif target_square.has_ally_piece(piece.color):
                            break

                    else:
                        break  # Not on board

                    possible_move_row += row_inc
                    possible_move_col += col_inc

        def king_moves():
            possible_moves = [  # Coded in a way that y is determined before x
                # Go through clockwise all adjacent
                (row - 1, col),
                (row - 1, col + 1),
                (row, col + 1),
                (row + 1, col + 1),
                (row + 1, col),
                (row + 1, col - 1),
                (row, col - 1),
                (row - 1, col - 1),
            ]

            for possible_move in possible_moves:
                possible_row, possible_col = possible_move

                if Square.in_range(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].is_empty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                            # Create temporary board to test if move gets king out of check
                            temp_board = copy.deepcopy(self)
                            temp_piece = copy.deepcopy(piece)
                            temp_board.move(temp_piece, move, testing=True)

                            # Check if king would still be in check after this move
                            king_pos = None
                            for r in range(ROWS):
                                for c in range(COLS):
                                    if isinstance(temp_board.squares[r][c].piece, King) and temp_board.squares[r][
                                        c].piece.color == piece.color:
                                        king_pos = (r, c)
                                        break

                            if king_pos:
                                in_check = False
                                for r in range(ROWS):
                                    for c in range(COLS):
                                        enemy_piece = temp_board.squares[r][c].piece
                                        if enemy_piece and enemy_piece.color != piece.color:
                                            temp_board.calc_moves(enemy_piece, r, c, bool=False)
                                            for m in enemy_piece.valid_moves:
                                                if m.final.row == king_pos[0] and m.final.col == king_pos[1]:
                                                    in_check = True
                                                    break
                                            if in_check:
                                                break
                                if not in_check:
                                    piece.add_move(move)
                        else:
                            piece.add_move(move)
                            
            # Will implement castling
            # You cannot castle if the king has already moved, or if the rook in question has moved. Nor can you castle while in check.
            # However, you can castle with a rook that is under attack at the time, and the rook can pass through an attacked square when castling while the king cannot.
            if not piece.moved:
                # Long castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4): # Iterate through the between cols
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                # Assigns left rook reference
                                piece.left_rook = left_rook
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                rook_move = Move(initial, final)

                                # Left king
                                initial = Square(row, col)
                                final = Square(row, 2)
                                king_move = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, king_move) and not self.in_check(left_rook, rook_move):
                                        left_rook.add_move(rook_move)
                                        piece.add_move(king_move)
                                else:
                                    left_rook.add_move(rook_move)
                                    piece.add_move(king_move)

                right_rook = self.squares[row][ROWS - 1].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7): # Iterate through the between cols
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                # Assigns right rook reference
                                piece.right_rook = right_rook
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                rook_move = Move(initial, final)

                                initial = Square(row, col)
                                final = Square(row, 6)
                                king_move = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, king_move) and not self.in_check(right_rook, rook_move):
                                        right_rook.add_move(rook_move)
                                        piece.add_move(king_move)
                                else:
                                    right_rook.add_move(rook_move)
                                    piece.add_move(king_move)


        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1, 1),  # Top Right
                (-1, -1),  # Top Left
                (1, 1),  # Bottom Right
                (1, -1)  # Bottom Left
            ])
        elif isinstance(piece, Rook):
            straight_line_moves([
                (-1, 0),  # Up
                (0, 1),  # Right
                (1, 0),  # Bottom
                (0, -1)  # Left
            ])
        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1, 1),  # Top Right
                (-1, -1),  # Top Left
                (1, 1),  # Bottom Right
                (1, -1),  # Bottom Left
                (-1, 0),  # Up
                (0, 1),  # Right
                (1, 0),  # Bottom
                (0, -1)  # Left
            ])
        elif isinstance(piece, King):
            king_moves()

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

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # Update the console board and reflect changes on GUI
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Pawn promotion handled in #Game
        piece.moved = True  # For pawns and castling

        # Pawn captures using en passant

        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                if not testing:
                    SoundManager().play("capture")


        # Castling
        elif isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.valid_moves[-1])
                SoundManager().play("castle")



        # Clear valid moves for update
        piece.clear_moves()

        # Set last move
        self.last_move = move

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2 # If king moves 2 squares == king castled
    def en_passant(self, initial, final):
        return abs(initial.row - final.row) == 2 # If the pawn moved 2 squares == first move

    def set_true_en_passant(self, piece):
        if isinstance(piece, Pawn):
            for row in range(ROWS):
                for col in range(COLS):
                    if isinstance(self.squares[row][col].piece, Pawn):
                        self.squares[row][col].piece.en_passant = False # Sets all en passant state to false
                    if self.en_passant(self.last_move.initial, self.last_move.final):
                        # Checks if the last pawn was moved 2
                        piece.en_passant = True # Then sets the previously moved en passant to True

    def _create(self):  # Underscore to imply private method
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (COLS - 2, COLS - 1) if color == "white" else (1, 0)

        # ALL pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            # self.squares[4][col] = Square(row_pawn, col, Pawn(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))