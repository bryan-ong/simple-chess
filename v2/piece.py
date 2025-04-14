import os.path

import pygame

from const import *


class Piece:
    def __init__(self, color, board, texture=None, texture_rect=None):
        self.color = color
        self.valid_moves = []
        self.moved = False
        self.board = board
        self.texture = texture
        self.texture = os.path.join(
            f"{IMAGE_DIR}\\{self.color}_{self.__class__.__name__.lower()}.png"
        )
        self.texture_rect = texture_rect
        self.is_dragged = False
        self.should_promote = False

    def get_surf_with_size(self, texture, size):
        return pygame.transform.scale(pygame.image.load(texture).convert_alpha(), (size, size)) # Apparently convert_alpha() makes the game run smoother

    def add_move(self, move):
        self.valid_moves.append(move)

    def clear_moves(self):
        self.valid_moves = []

    def __str__(self):
        return f"""
Name: {self.__class__.__name__.lower()}
Color: {self.color}
Moved: {self.moved}
        """

class Pawn(Piece):
    def __init__(self, color, board):
        # -1 is up on the Y-axis in pygame
        self.dir = -1 if color == "white" else 1  # I plan to add more colors in the future for more players


        self.can_get_passant_by_other = False
        super().__init__(color, board)  # Material values

class Knight(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)  # For AI prioritization


class Bishop(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)  # For AI prioritization


class Rook(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)  # For AI prioritization


class Queen(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)  # For AI prioritization


class King(Piece):
    def __init__(self, color, board):
        self.left_rook = None
        self.right_rook = None
        super().__init__(color, board)  # For AI prioritization
