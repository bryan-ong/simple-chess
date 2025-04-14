import os
from const import *
from square import Square
from move import Move
dir_dict = {
    "white": (0, -1),
    "black": (0, 1),
}

class Piece:
    def __init__(self, pos, color, board, owner):
        self.col = pos(0)
        self.row = pos(1)
        self.moved = False
        self.color = color
        self.texture = os.path.join(
            f"{IMAGE_DIR}\\{self.color}_{self.__class__.__name__.lower()}.png"
        )
        self.valid_moves = []
        self.board = board
        self.owner = owner

    def move(self):
        pass

class Pawn(Piece):
    def __init__(self, pos, color):
        self.should_promote = False
        self.can_get_passant_by_other = False
        self.direction = dir_dict[self.color]

        super().__init__(pos, color)

    def get_possible_moves(self):
        col = self.col
        row = self.row
        board = self.board
        direction = self.direction  # 1 for white (down), -1 for black (up)

        max_steps = 2 if not self.moved else 1

        for move_step in range(1, max_steps + 1):
                final_row = row + (direction * move_step)
                if Square.in_range(move_step):

                # Check if still on board

                # Check if square is empty
                if board.squares[final_row][col].is_empty():
                    initial, final = Square(row, col), Square(final_row, col)
                    move = Move(initial, final)

                    if bool:
                        if not self.in_check(piece, move):
                            self.valid_moves.append(move)
                    else:
                        self.valid_moves.append(move)
                else:
                    break  # Blocked by piece
            else:
                break

        # Diagonal captures
        possible_move_rows = [row + direction]
        possible_move_cols = [col - 1, col + 1]

        for move_step in possible_move_rows:
            for possible_move_col in possible_move_cols:
                # Check if on board
                if Square.in_range(move_step, possible_move_col):
                    if board.squares[move_step][possible_move_col].has_enemy_piece(piece.color):
                        final_piece = board.squares[move_step][possible_move_col].piece
                        initial, final = Square(row, col), Square(move_step, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                self.valid_moves.append(move)
                        else:
                            self.valid_moves.append(move)

        # En passant moves
        r = 3 if piece.color == "white" else ROWS - 4
        final_r = 2 if piece.color == "white" else 5
        if row == r:
            # Left
            if Square.in_range(col - 1):
                if board.squares[row][col - 1].has_enemy_piece(piece.color):
                    left_pawn = board.squares[row][col - 1].piece
                    if isinstance(left_pawn, Pawn):
                        if left_pawn.can_get_passant_by_other:
                            # print("left can passant")
                            initial, final = Square(row, col), Square((final_r, col - 1), left_pawn)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move):
                                    self.valid_moves.append(move)
                            else:
                                self.valid_moves.append(move)
            # Right
            if Square.in_range(col + 1):
                if board.squares[row][col + 1].has_enemy_piece(self.color):
                    right_pawn = board.squares[row][col + 1].piece
                    if isinstance(right_pawn, Pawn):
                        # print("right ", right_pawn.en_passant)
                        if right_pawn.can_get_passant_by_other:
                            initial, final = Square(row, col), Square((final_r, col + 1), right_pawn)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move):
                                    self.valid_moves.append(move)
                            else:
                                self.valid_moves.append(move)


    def filter_valid_moves(self, valid_moves):
        pass