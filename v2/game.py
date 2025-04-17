import os.path

import pygame

import v2.chesstimer
from board import *
from dragger import Dragger
from config import Config
from square import Square
from piece import *
from button import Button
from soundmanager import SoundManager
from chesstimer import ChessTimer
from const import *
class Game:



    def __init__(self, screen):
        self.board = Board(2)
        self.dragger = Dragger(BOARD_START_X, BOARD_START_Y)
        self.next_player = "white"
        self.hovered_square = None
        self.config = Config()
        self.promotion_buttons = []
        self.surface = screen
        SoundManager().set_config(self.config)
        self.last_dragged_piece = None
        self.last_dragged_pos = None
        self.font_monospace = pygame.font.SysFont('monospace', 38, bold=True)
        self.font_segoe = pygame.font.SysFont('segoeui', 28, bold=True)

        self.checkmate_prompt = Button(
            text="",
            width=200,
            height=150,
            pos=(SCR_WIDTH // 2, SCR_HEIGHT // 2),
            action=lambda: print("hello")
        )

        self.turn_indicator_white = pygame.Rect(
            BOARD_START_X - BORDER_RADIUS * 2,
            BOARD_START_Y + BOARD_WIDTH / 2 + BORDER_RADIUS * 2,
            BOARD_WIDTH + BORDER_RADIUS * 2 * 2,
            BOARD_WIDTH / 2)

        self.turn_indicator_black = pygame.Rect(
            BOARD_START_X - BORDER_RADIUS * 2,
            BOARD_START_Y - BORDER_RADIUS * 2,
            BOARD_WIDTH + BORDER_RADIUS * 2 * 2,
            BOARD_WIDTH / 2)

        self.darkened_color = tuple(i * (0.95 - self.config.theme.shadow_opacity) for i in self.config.theme.bg.dark)

        self.exit_button = Button(
            image=exit_image,
            width=40,
            height=40,
            pos=(SCR_WIDTH - 40, 0),
            hover_color=RED,
            action=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
        )
        self.minimize_button = Button(
            image=minimize_image,
            width=40,
            height=40,
            pos=(SCR_WIDTH - 80, 0),
            hover_color=RED,
            action=lambda: pygame.event.post(pygame.event.Event(pygame.display.iconify()))
        )

        self.bg_rect = pygame.Rect(0, 0, SCR_WIDTH, SCR_HEIGHT)
        self.top_bar = pygame.Rect(0, 0, SCR_WIDTH, 40)

        self.black_timer = pygame.Rect((SCR_WIDTH - SQSIZE) // 2, BOARD_START_Y - (BORDER_RADIUS * 3), SQSIZE, BORDER_RADIUS * 3)
        self.white_timer = pygame.Rect((SCR_WIDTH - SQSIZE) // 2, BOARD_START_Y + BOARD_HEIGHT, SQSIZE, BORDER_RADIUS * 3)




    def show_timer(self):

        pygame.draw.rect(self.surface, self.config.theme.board_border.dark, self.black_timer, border_top_left_radius=BORDER_RADIUS, border_top_right_radius=BORDER_RADIUS)
        pygame.draw.rect(self.surface, self.config.theme.board_border.light, self.white_timer, border_bottom_left_radius=BORDER_RADIUS, border_bottom_right_radius=BORDER_RADIUS)

        black_time_surf = self.font_segoe.render(
            self.board.timer.get_simple_formatted_time("black"),
            True,
            self.config.theme.board_border.light
        )

        white_time_surf = self.font_segoe.render(
            self.board.timer.get_simple_formatted_time("white"),
            True,
            self.config.theme.board_border.dark
        )

        black_time_rect = black_time_surf.get_rect(center=(BOARD_START_X + BOARD_WIDTH // 2, BOARD_START_Y - BORDER_RADIUS * 3 // 2))
        self.surface.blit(black_time_surf, black_time_rect)
        white_time_rect = white_time_surf.get_rect(center=(BOARD_START_X + BOARD_WIDTH // 2, BOARD_START_Y + BOARD_HEIGHT + BORDER_RADIUS * 3 // 2))
        self.surface.blit(white_time_surf, white_time_rect)


    def show_gui(self):
        theme = self.config.theme

        pygame.draw.rect(self.surface, theme.bg.dark, self.bg_rect)

        self.darkened_color = tuple(i * (0.95 - self.config.theme.shadow_opacity) for i in self.config.theme.bg.dark)

        pygame.draw.rect(self.surface, self.darkened_color, self.top_bar)



        self.exit_button.draw_and_handle(self.surface)
        self.minimize_button.draw_and_handle(self.surface)

        title_surf = self.font_monospace.render("Chess", True, theme.bg.light)

        self.surface.blit(title_surf, (10, 0))


    def show_checkmate(self, shadow_surface):
        if self.board.checkmated:
            self.darken_area(shadow_surface, (0, 40), (SCR_WIDTH, SCR_HEIGHT - 40))



        # reset_button = Button(
        #     text="New Game",
        #     width=90,
        #     height=50,
        #     action=lambda : self.board.__init__(2)
        # )

        # self.checkmate_prompt.draw_and_handle(self.surface, True)

    def show_board_misc(self):
        theme = self.config.theme
        border_radius = BORDER_RADIUS if theme.rounded else 0
        # Board border
        pygame.draw.rect(self.surface, theme.board_border.dark, (
            BOARD_START_X - BORDER_RADIUS,
            BOARD_START_Y - BORDER_RADIUS,
            BOARD_WIDTH + BORDER_RADIUS * 2,
            BOARD_HEIGHT // 2 + BORDER_RADIUS * 2), border_top_left_radius=border_radius, border_top_right_radius=border_radius)

        pygame.draw.rect(self.surface, theme.board_border.light, (
            BOARD_START_X - BORDER_RADIUS,
            BOARD_START_Y + BOARD_HEIGHT // 2,
            BOARD_WIDTH + BORDER_RADIUS * 2,
            BOARD_HEIGHT // 2 + BORDER_RADIUS), border_bottom_left_radius=border_radius, border_bottom_right_radius=border_radius)

    def show_turn_indicator(self):
        color = self.config.theme.turn_indicator.light

        pygame.draw.rect(self.surface, color, self.turn_indicator_white if self.next_player == "black" else self.turn_indicator_black, border_radius=BORDER_RADIUS * 2)


    def show_bg(self):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # Color from theme
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark


                if theme.rounded:
                    kwargs = {}
                    if row == 0 and col == 0:
                        kwargs['border_top_left_radius'] = BORDER_RADIUS
                    elif row == 0 and col == COLS - 1:
                        kwargs['border_top_right_radius'] = BORDER_RADIUS
                    elif row == ROWS - 1 and col == 0:
                        kwargs['border_bottom_left_radius'] = BORDER_RADIUS
                    elif row == ROWS - 1 and col == COLS - 1:
                        kwargs['border_bottom_right_radius'] = BORDER_RADIUS

                    if kwargs:
                        pygame.draw.rect(self.surface, color, (col * SQSIZE + BOARD_START_X, row * SQSIZE + BOARD_START_Y, SQSIZE, SQSIZE), **kwargs)
                        continue

                pygame.draw.rect(self.surface, color, (col * SQSIZE + BOARD_START_X, row * SQSIZE + BOARD_START_Y, SQSIZE, SQSIZE))


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
                square = self.board.squares[row][col]
                if not square.has_piece():
                    continue

                piece = square.piece
                size = SELECTED_PIECE_SIZE if piece.is_dragged else PIECE_SIZE

                # Get or create texture
                if not hasattr(piece, '_cached_texture') or piece._cached_size != size:
                    piece._cached_texture = piece.get_surf_with_size(piece.texture, size)
                    piece._cached_size = size
                    piece.texture_rect = piece._cached_texture.get_rect()

                # Calculate position
                if piece.is_dragged:
                    pos = pygame.mouse.get_pos()
                else:
                    pos = (
                        col * SQSIZE + BOARD_START_X + SQSIZE // 2,
                        row * SQSIZE + BOARD_START_Y + SQSIZE // 2
                    )

                piece.texture_rect.center = pos
                self.surface.blit(piece._cached_texture, piece.texture_rect)

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

                x = pos.col * SQSIZE + BOARD_START_X
                y = pos.row * SQSIZE + BOARD_START_Y

                if theme.rounded:
                    if pos.row == 0 and pos.col == 0:
                        pygame.draw.rect(self.surface, color, (x, y, SQSIZE, SQSIZE),
                                         border_top_left_radius=BORDER_RADIUS)
                    elif pos.row == 0 and pos.col == COLS - 1:
                        pygame.draw.rect(self.surface, color, (x, y, SQSIZE, SQSIZE),
                                         border_top_right_radius=BORDER_RADIUS)
                    elif pos.row == ROWS - 1 and pos.col == 0:
                        pygame.draw.rect(self.surface, color, (x, y, SQSIZE, SQSIZE),
                                         border_bottom_left_radius=BORDER_RADIUS)
                    elif pos.row == ROWS - 1 and pos.col == COLS - 1:
                        pygame.draw.rect(self.surface, color, (x, y, SQSIZE, SQSIZE),
                                         border_bottom_right_radius=BORDER_RADIUS)
                    else:
                        pygame.draw.rect(self.surface, color, (x, y, SQSIZE, SQSIZE))
                else:
                    pygame.draw.rect(self.surface, color, (x, y, SQSIZE, SQSIZE))


    def show_hover(self):
        if self.hovered_square:
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)

            pygame.draw.rect(self.surface, HOVERED_SQUARE_COLOR, rect, width=SQSIZE // 20)

    def darken_area(self, shadow_surface, dest=(0,0), size=(100, 100)):

        shadow_surface.fill((0, 0, 0, 0))
        shadow_surface.set_alpha(255 * (self.config.theme.shadow_opacity * 2))

        pygame.draw.rect(shadow_surface, "black", (
            0, 0, size[0], size[1]
        ))

        self.surface.blit(shadow_surface, (dest[0], dest[1]))

    def show_promotion(self, shadow_surface):
        if not self.board.pending_promotion:
            return
        self.board.timer.pause()
        theme = self.config.theme
        if self.board.last_move is not None:
            if isinstance(self.dragger.piece, Pawn):
                piece = self.dragger.piece
                if piece.should_promote:
                    final = self.board.last_move.final
                    row, col = final.row, final.col
                    brightened_color = tuple(min(255, int(channel + 25)) for channel in theme.bg.light)

                    self.darken_area(shadow_surface, (BOARD_START_X, BOARD_START_Y), (BOARD_WIDTH, BOARD_HEIGHT))
                    # I am going to try something ( Had 4 separate button initializations, very similar so it can be done in a for loop )
                    def create_promotion_callback(piece, final, Piece_class):
                        return lambda: [
                            self.board.set_promote_piece(piece, final, Piece_class),
                            self.remove_promote_buttons(),
                            self.board.timer.start(self.next_player)
                        ]

                    # Without a callback python will always use the latest iteration which is Knight for the action
                    for idx, Piece_class in enumerate([Queen, Bishop, Rook, Knight]):
                        button = Button(
                            image=piece.get_surf_with_size(Piece_class(piece.color).texture, PIECE_SIZE), width=SQSIZE,
                            height=SQSIZE, bg_color=theme.bg.light, hover_color=brightened_color,
                            pos=(col * SQSIZE + BOARD_START_X,
                                 (row + idx if piece.color == "white" else (-idx - 1)) * SQSIZE + BOARD_START_Y + (
                                     0 if piece.color == "white" else BOARD_HEIGHT)),
                            action=create_promotion_callback(piece, final, Piece_class)
                        )
                        self.promotion_buttons.append(button)

                    for btn in self.promotion_buttons:
                        btn.draw_and_handle(self.surface)


    # Non-render methods
    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"
        self.board.timer.active_player = self.next_player

    def set_hover(self, row, col):
        pass
        # self.hovered_square = self.board.squares[row][col]


    def change_theme(self):
        self.config.change_theme()

    def randomize_theme(self):
        self.config.randomize_theme()


    def reset(self):
        self.__init__(self.surface)


    def remove_promote_buttons(self):
        for button in self.promotion_buttons:
            button.remove_button()
