import os.path

import pygame

from const import *


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == "white" else -1  # For AI to recognize
        self.value = value * value_sign
        self.valid_moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        self.is_dragged = False
        self.should_promote = False

    def set_texture(self):
        self.texture = os.path.join(
            f"assets/images/{self.color}_{self.name}.png"
        )

    def get_surf_with_size(self, texture, size):
        return pygame.transform.scale(pygame.image.load(texture), (size, size))

    def add_move(self, move):
        self.valid_moves.append(move)

    def clear_moves(self):
        self.valid_moves = []

    def __str__(self):
        return f"""
Name: {self.name}
Color: {self.color}
Moved: {self.moved}
        """

class Pawn(Piece):  # First time using inheritance for python
    def __init__(self, color):
        # -1 is up on the Y-axis in pygame
        self.dir = -1 if color == "white" else 1  # I plan to add more colors in the future for more players
        self.en_passant = False
        super().__init__("pawn", color, 1.0)  # Material values


class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color, 3.0)  # For AI prioritization


class Bishop(Piece):
    def __init__(self, color):
        super().__init__("bishop", color, 3.001)  # For AI prioritization


class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color, 5)  # For AI prioritization


class Queen(Piece):
    def __init__(self, color):
        super().__init__("queen", color, 9)  # For AI prioritization


class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", color, 1000)  # For AI prioritization
