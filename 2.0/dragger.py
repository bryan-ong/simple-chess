import pygame
from const import *

class Dragger:
    def __init__(self, board_offset_x=0, board_offset_y=0):
        self.mouseX = 0
        self.mouseY = 0
        self.dragging = False
        self.piece = None
        self.initial_row = 0
        self.initial_col = 0
        self.board_offset_x = board_offset_x  # X offset where the board is rendered
        self.board_offset_y = board_offset_y
    # def update_blit(self):
    #     self.piece.is_dragged = True


    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        adjusted_x = pos[0] - self.board_offset_x
        adjusted_y = pos[1] - self.board_offset_y
        self.initial_col = adjusted_x // SQSIZE # Save initial position for when move is invalid, resets position
        self.initial_row = adjusted_y // SQSIZE

    def drag_piece(self, piece):
        # Original method used a different image and texture rect to enlarge and change center using update_blit(),
        # but I have decided to just assign an attribute to piece and handle the logic there, this allows for dynamic changing of size without limits
        self.piece = piece
        self.dragging = True
        piece.is_dragged = True

    def undrag_piece(self):
        self.dragging = False
        self.piece.is_dragged = False

    def get_adjusted_pos(self, pos=None):
        if pos is None:
            pos = (self.mouseX, self.mouseY)
        return pos[0] - BOARD_START_X, pos[1] - BOARD_START_Y

    def grid_coords(self, pos=None):
        if pos is None:
            pos = (self.mouseX, self.mouseY)
        adjusted_x = pos[0] - self.board_offset_x
        adjusted_y = pos[1] - self.board_offset_y
        row = adjusted_y // SQSIZE
        col = adjusted_x // SQSIZE
        return row, col