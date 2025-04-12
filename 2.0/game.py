import os.path

import pygame
import self

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from piece import *
from button import Button
from soundmanager import SoundManager

class Game:
    SCR_WIDTH = None
    SCR_HEIGHT = None

    @classmethod
    def init_class_vars(cls, screen):
        cls.SCR_WIDTH = screen.get_width()

    def __init__(self, screen):
        if Game.SCR_WIDTH is None:
            Game.init_class_vars(screen) # Ensure we init HEIGHT and WIDTH

        self.board = Board()
        self.dragger = Dragger(BOARD_START_X, BOARD_START_Y)
        self.next_player = "white"
        self.hovered_square = None
        self.config = Config()
        self.promotion_buttons = []
        self.surface = screen
        SoundManager().set_config(self.config)

        # Render methods
    def show_gui(self):
        theme = self.config.theme
        rect = pygame.Rect(0,0, self.surface.get_width(), self.surface.get_height())

        pygame.draw.rect(self.surface, theme.bg.dark, rect)

    def show_bg(self):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # Color from theme
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark

                rect = pygame.Rect(col * SQSIZE + BOARD_START_X, row * SQSIZE + BOARD_START_Y, SQSIZE, SQSIZE)
                pygame.draw.rect(self.surface, color, rect)



    def show_coords(self):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # Row coords
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS - row), True, color)
                    lbl_pos = (SQSIZE // 20 + BOARD_START_X, SQSIZE // 20 + row * SQSIZE + BOARD_START_Y)
                    self.surface.blit(lbl, lbl_pos)

                # Col coords
                if row == ROWS - 1:
                    color = theme.bg.light if col % 2 == 0 else theme.bg.dark
                    lbl = self.config.font.render(Square.get_alpha_col(col), True, color)
                    lbl_pos = (col * SQSIZE + SQSIZE * 0.8 + BOARD_START_X, BOARD_HEIGHT - SQSIZE // 4 + BOARD_START_Y)
                    self.surface.blit(lbl, lbl_pos)

    def show_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    rendered_size = PIECE_SIZE if piece.is_dragged == False else SELECTED_PIECE_SIZE

                    img = piece.get_surf_with_size(piece.texture, rendered_size)
                    img_center = col * SQSIZE + SQSIZE / 2 + BOARD_START_X, row * SQSIZE + SQSIZE / 2 + BOARD_START_Y  # Center image

                    piece.texture_rect = img.get_rect(
                        center=img_center if not piece.is_dragged else pygame.mouse.get_pos())

                    self.surface.blit(img, piece.texture_rect)

    def show_moves(self, shadow_surface):
        theme = self.config.theme
        shadow_surface.fill((0, 0, 0, 0))
        shadow_surface.set_alpha(255 * theme.shadow_opacity)

        if self.dragger.dragging:
            piece = self.dragger.piece

            # Iterate through all valid moves
            for move in piece.valid_moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark

                x = move.final.col * SQSIZE + SQSIZE // 2
                y = move.final.row * SQSIZE + SQSIZE // 2

                if self.board.squares[move.final.row][move.final.col].has_enemy_piece(piece.color):
                    pygame.draw.circle(shadow_surface, color, (
                        x, y,
                    ), SQSIZE // 2, width=int(SQSIZE // 11.5))
                else:
                    pygame.draw.circle(shadow_surface, color, (
                        x,
                        y,
                    ), SQSIZE * 0.175)
        self.surface.blit(shadow_surface, (BOARD_START_X, BOARD_START_Y))

    def show_last_move(self):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark

                rect = (pos.col * SQSIZE + BOARD_START_X, pos.row * SQSIZE + BOARD_START_Y, SQSIZE, SQSIZE)
                pygame.draw.rect(self.surface, color, rect)

    def show_hover(self):
        if self.hovered_square:
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)

            pygame.draw.rect(self.surface, HOVERED_SQUARE_COLOR, rect, width=SQSIZE // 20)

    def show_promotion(self, shadow_surface):
        if not self.board.pending_promotion:
            return

        theme = self.config.theme
        if self.board.last_move is not None:
            if isinstance(self.dragger.piece, Pawn):
                piece = self.dragger.piece
                if piece.should_promote:
                    final = self.board.last_move.final
                    row, col = final.row, final.col
                    center_row, center_col = ROWS // 2, COLS // 2
                    # Gets the direction to draw in, i.e the center
                    draw_dir = (
                        1 if col < center_col else -1,
                        1 if row < center_row else -1
                    )

                    # Calculate position based on quadrant
                    if draw_dir == (1, 1):  # Top-left
                        rect_pos = (col + 1, row + 0)
                    elif draw_dir == (-1, 1):  # Top-right
                        rect_pos = (col - 1, row + 0)
                    elif draw_dir == (1, -1):  # Bottom-left
                        rect_pos = (col + 1, row - 3)
                    else:  # Bottom-right
                        rect_pos = (col - 1, row - 3)

                    brightened_color = tuple(min(255, int(channel + 50)) for channel in theme.bg.light)

                    shadow_surface.fill((0, 0, 0, 0))
                    shadow_surface.set_alpha(255 * (theme.shadow_opacity * 2))

                    pygame.draw.rect(shadow_surface, "black", (
                        BOARD_START_X, BOARD_START_Y, BOARD_WIDTH, BOARD_HEIGHT
                    ))

                    self.surface.blit(shadow_surface, (BOARD_START_X, BOARD_START_Y))

                    # queen_btn = Button(
                    #     image=piece.get_surf_with_size(Queen(piece.color).texture, PIECE_SIZE), width=SQSIZE, height=SQSIZE, bg_color=brightened_color,
                    #     pos=(rect_pos[0] * SQSIZE,
                    #          rect_pos[1] * SQSIZE,),
                    #     action=lambda: [self.board.set_promote_piece(piece, final, Queen), self.remove_promote_buttons()]
                    # )
                    # bishop_btn = Button(
                    #     image=piece.get_surf_with_size(Bishop(piece.color).texture, PIECE_SIZE), width=SQSIZE, height=SQSIZE, bg_color=brightened_color,
                    #     pos=(rect_pos[0] * SQSIZE,
                    #          (rect_pos[1] + 1) * SQSIZE,),
                    #     action=lambda: [self.board.set_promote_piece(piece, final, Bishop), self.remove_promote_buttons()]
                    # )
                    # rook_btn = Button(
                    #     image=piece.get_surf_with_size(Rook(piece.color).texture, PIECE_SIZE), width=SQSIZE, height=SQSIZE, bg_color=brightened_color,
                    #     pos=(rect_pos[0] * SQSIZE,
                    #          (rect_pos[1] + 2) * SQSIZE,),
                    #     action=lambda: [self.board.set_promote_piece(piece, final, Rook), self.remove_promote_buttons()]
                    # )
                    #
                    # knight_btn = Button(
                    #     image=piece.get_surf_with_size(Knight(piece.color).texture, PIECE_SIZE), width=SQSIZE, height=SQSIZE, bg_color=brightened_color,
                    #     pos=(rect_pos[0] * SQSIZE,
                    #          (rect_pos[1] + 3) * SQSIZE,),
                    #     action=lambda: [self.board.set_promote_piece(piece, final, Knight), self.remove_promote_buttons()]
                    # )

                    # I am going to try something

                    def create_promotion_callback(piece, final, Piece_class):
                        return lambda: [
                            self.board.set_promote_piece(piece, final, Piece_class),
                            self.remove_promote_buttons()
                        ]
                    # Without a callback python will always use the latest iteration which is Knight for the action
                    for idx, Piece_class in enumerate([Queen, Bishop, Rook, Knight]):
                        button = Button(
                            image=piece.get_surf_with_size(Piece_class(piece.color).texture, PIECE_SIZE), width=SQSIZE, height=SQSIZE, bg_color=brightened_color,
                                pos=(rect_pos[0] * SQSIZE + BOARD_START_X,
                                     (rect_pos[1] + idx) * SQSIZE + BOARD_START_Y,),
                                action=create_promotion_callback(piece, final, Piece_class)
                        )
                        self.promotion_buttons.append(button)


                    for btn in self.promotion_buttons:
                        btn.draw(self.surface)
                        btn.handle_event()


    # Non-render methods
    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def set_hover(self, row, col):
        pass
        # self.hovered_square = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def reset(self):
        self.__init__(self.surface)

    def remove_promote_buttons(self):
        for button in self.promotion_buttons:
            button.remove_button()