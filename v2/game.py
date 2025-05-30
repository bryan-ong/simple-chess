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

    def __init__(self, main, screen, config, init_time_mins, inc_time_secs):
        self.main = main
        self.init_time_mins = init_time_mins
        self.inc_time_secs = inc_time_secs
        self.board = Board(2, init_time_mins, inc_time_secs)
        self.dragger = Dragger(BOARD_START_X, BOARD_START_Y)
        self.next_player = "white"
        self.hovered_square = None
        self.config = config
        self.promotion_buttons = []
        self.surface = screen
        SoundManager().set_config(self.config)
        self.last_dragged_piece = None
        self.last_dragged_pos = None
        self.font_monospace = pygame.font.SysFont('monospace', 38, bold=True)
        self.font_segoe = pygame.font.SysFont('segoeui', 28, bold=True)
        self.font_corbel = pygame.font.SysFont('corbel', 28)
        self.font_corbel_small = pygame.font.SysFont('corbel', 20)
        self.update_colors()

    def show_timer(self):

        pygame.draw.rect(self.surface, self.config.theme.board_border.dark, self.black_timer,
                         border_top_left_radius=BORDER_RADIUS, border_top_right_radius=BORDER_RADIUS)
        pygame.draw.rect(self.surface, self.config.theme.board_border.light, self.white_timer,
                         border_bottom_left_radius=BORDER_RADIUS, border_bottom_right_radius=BORDER_RADIUS)

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

        black_time_rect = black_time_surf.get_rect(
            center=(BOARD_START_X + BOARD_WIDTH // 2, BOARD_START_Y - BORDER_RADIUS * 3 // 2))
        self.surface.blit(black_time_surf, black_time_rect)
        white_time_rect = white_time_surf.get_rect(
            center=(BOARD_START_X + BOARD_WIDTH // 2, BOARD_START_Y + BOARD_HEIGHT + BORDER_RADIUS * 3 // 2))
        self.surface.blit(white_time_surf, white_time_rect)

        for btn in self.time_control_btns:
            btn.draw_and_handle(self.surface)



    def show_gui(self):
        theme = self.config.theme

        # Main bg
        pygame.draw.rect(self.surface, theme.bg.dark, self.bg_rect)

        self.darkened_color = tuple(i * (0.95 - self.config.theme.shadow_opacity) for i in self.config.theme.bg.dark)
        self.darker_color = tuple(i * (0.8 - self.config.theme.shadow_opacity) for i in self.config.theme.bg.dark)

        # Top bar
        pygame.draw.rect(self.surface, self.darkened_color, self.top_bar)

        self.exit_button.draw_and_handle(self.surface)
        self.minimize_button.draw_and_handle(self.surface)

        # Chess top-left
        self.surface.blit(self.font_monospace.render("Chess", True, theme.bg.light), (10, 0))
        self.show_left_sidebar()
        self.show_right_sidebar()

    def show_captured(self):
        size = 40
        white_mat_sum, black_mat_sum = 0, 0
        for i, piece in enumerate(self.board.captured_pieces_white):
            if not hasattr(piece, '_cached_texture') or piece._cached_size != size:
                piece._cached_texture = pygame.transform.rotate(piece.get_surf_with_size(piece.texture, size), 180)
                piece._cached_size = size
                piece.texture_rect = piece._cached_texture.get_rect()

                piece.texture_rect.center = (BOARD_START_X + i * size // 2 + size // 2, BOARD_START_Y + BOARD_HEIGHT + BORDER_RADIUS * 2.05)

            if isinstance(piece, Pawn):
                white_mat_sum += 1
            elif isinstance(piece, (Knight, Bishop)):
                white_mat_sum += 3
            elif isinstance(piece, Rook):
                white_mat_sum += 5
            elif isinstance(piece, Queen):
                white_mat_sum += 9

            self.surface.blit(piece._cached_texture, piece.texture_rect)
        self.surface.blit(pygame.font.SysFont('monospace', 24, bold=True).render(str(white_mat_sum if white_mat_sum != 0 else ""), True, self.config.theme.bg.light),
                          (BOARD_START_X + size // 2 + (size // 1.5 * len(self.board.captured_pieces_white)), BOARD_START_Y + BOARD_HEIGHT + BORDER_RADIUS))

        for i, piece in enumerate(self.board.captured_pieces_black):
            if not hasattr(piece, '_cached_texture') or piece._cached_size != size:
                piece._cached_texture = piece.get_surf_with_size(piece.texture, size)
                piece._cached_size = size
                piece.texture_rect = piece._cached_texture.get_rect()

                piece.texture_rect.center = (BOARD_START_X + i * size // 2 + size // 2, BOARD_START_Y - BORDER_RADIUS * 2)

            if isinstance(piece, Pawn):
                black_mat_sum += 1
            elif isinstance(piece, (Knight, Bishop)):
                black_mat_sum += 3
            elif isinstance(piece, Rook):
                black_mat_sum += 5
            elif isinstance(piece, Queen):
                black_mat_sum += 9

            self.surface.blit(piece._cached_texture, piece.texture_rect)
        self.surface.blit(pygame.font.SysFont('monospace', 24, bold=True).render(str(black_mat_sum if black_mat_sum != 0 else ""), True, self.config.theme.bg.light),
                          (BOARD_START_X + size // 2 + (size // 1.5 * len(self.board.captured_pieces_black)), BOARD_START_Y - BORDER_RADIUS * 2.5))

        # Now to get the difference in material


    def show_right_sidebar(self):
        pygame.draw.rect(self.surface, self.darker_color, self.right_sidebar)


    def show_left_sidebar(self):
        theme = self.config.theme
        # Game settings sidebar
        pygame.draw.rect(self.surface, self.darker_color, self.left_sidebar)
        # Game settings sidebar title
        self.surface.blit(self.font_corbel.render("Game Settings", True, theme.bg.light), (10, 40 + BORDER_RADIUS))

        self.surface.blit(self.font_corbel_small.render("Bullet", True, theme.bg.light), ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2 + 20, 110))
        self.surface.blit(self.bullet_icon, self.bullet_icon_rect)

        self.surface.blit(self.font_corbel_small.render("Blitz", True, theme.bg.light), ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2 + 20, 110 + BORDER_RADIUS * 6))
        self.surface.blit(self.blitz_icon, self.blitz_icon_rect)

        self.surface.blit(self.font_corbel_small.render("Rapid", True, theme.bg.light), ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2 + 20, 110 + BORDER_RADIUS * 6 * 2))
        self.surface.blit(self.rapid_icon, self.rapid_icon_rect)

        self.surface.blit(self.font_corbel_small.render("Custom", True, theme.bg.light), ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2 + 20, 110 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(self.custom_icon, self.custom_icon_rect)


        mins = self.font_corbel_small.render("Mins", True, theme.bg.light)
        mins_rect = mins.get_rect(center=(SIDEBAR_WIDTH // 4, 118 + 32 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(mins, mins_rect)

        secs = self.font_corbel_small.render("Secs", True, theme.bg.light)
        secs_rect = secs.get_rect(center=(SIDEBAR_WIDTH // 4 * 2, 118 + 32 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(secs, secs_rect)

        incr = self.font_corbel_small.render("Incr", True, theme.bg.light)
        incr_rect = incr.get_rect(center=(SIDEBAR_WIDTH // 4 * 3, 118 + 32 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(incr, incr_rect)



        min_count = self.font_corbel_small.render(str(int(self.init_time_mins)), True, theme.bg.light)
        min_count_rect = min_count.get_rect(center=(SIDEBAR_WIDTH // 4, 118 + 62 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(min_count, min_count_rect)

        # Modulo 1 extracts the remainder, aka the decimal part
        sec_count = self.font_corbel_small.render(str(int((self.init_time_mins % 1) * 60)), True, theme.bg.light)
        sec_count_rect = sec_count.get_rect(center=(SIDEBAR_WIDTH // 4 * 2, 118 + 62 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(sec_count, sec_count_rect)

        incr_count = self.font_corbel_small.render(str(self.inc_time_secs), True, theme.bg.light)
        incr_count_rect = incr_count.get_rect(center=(SIDEBAR_WIDTH // 4 * 3, 118 + 62 + BORDER_RADIUS * 6 * 3))
        self.surface.blit(incr_count, incr_count_rect)

        text = self.font_corbel_small.render("Change", True, theme.bg.light)
        text_rect = text.get_rect(center=(SIDEBAR_WIDTH // 4 * 2, 118 + 12 + (SCR_HEIGHT - 40) // 2))
        self.surface.blit(text, text_rect)
        text = self.font_corbel_small.render("Theme", True, theme.bg.light)
        text_rect = text.get_rect(center=(SIDEBAR_WIDTH // 4 * 2, 118 + 32 + (SCR_HEIGHT - 40) // 2))
        self.surface.blit(text, text_rect)

        self.surface.blit(self.font_corbel.render("Theme Settings", True, theme.bg.light), (10, 40 + BORDER_RADIUS + (SCR_HEIGHT - 40) // 2))




    def show_game_end(self, shadow_surface):
        theme = self.config.theme
        if self.board.game_over:
            self.darken_area(shadow_surface, (0, 40), (SCR_WIDTH, SCR_HEIGHT - 40))
            pygame.draw.rect(self.surface, theme.bg.light, self.game_end_rect, border_radius=BORDER_RADIUS if theme.rounded else 0)
            self.reset_button.draw_and_handle(self.surface)
            end_type = None
            winner = None
            if self.board.checkmated:
                end_type = self.font_segoe.render("Checkmate!", True, theme.bg.dark)
                winner = self.font_segoe.render(f"{self.board.winner.capitalize()} wins!".upper(), True, theme.bg.dark)
            elif self.board.stalemated:
                end_type = self.font_segoe.render("Stalemate!", True, theme.bg.dark)
                winner = self.font_segoe.render("Draw", True, theme.bg.dark)
            elif self.board.drew:
                end_type = self.font_segoe.render("Draw!", True, theme.bg.dark)
            elif self.board.timer.is_timeout():
                end_type = self.font_segoe.render("Timeout!", True, theme.bg.dark)
                winner = self.font_segoe.render(f"{self.board.winner.capitalize()} wins!".upper(), True, theme.bg.dark)

            if end_type and not winner: # I know I'm only calling this method when the game ends, but just in case...
                # If game ends and no winner = draw, I need to center it nicely since there's no winner text
                end_type_rect = end_type.get_rect(center=(SCR_WIDTH // 2, SCR_HEIGHT // 2 - SQSIZE // 2))
                self.surface.blit(end_type, end_type_rect)

            elif end_type and winner: # This one I do need to check though
                end_type_rect = end_type.get_rect(center=(SCR_WIDTH // 2, SCR_HEIGHT // 2 - SQSIZE))
                self.surface.blit(end_type, end_type_rect)

                winner_rect = winner.get_rect(center=(SCR_WIDTH // 2, SCR_HEIGHT // 2))
                self.surface.blit(winner, winner_rect)

    def show_board_misc(self):
        theme = self.config.theme
        border_radius = BORDER_RADIUS if theme.rounded else 0
        # Board border
        pygame.draw.rect(self.surface, theme.board_border.dark, (
            BOARD_START_X - BORDER_RADIUS,
            BOARD_START_Y - BORDER_RADIUS,
            BOARD_WIDTH + BORDER_RADIUS * 2,
            BOARD_HEIGHT // 2 + BORDER_RADIUS * 2), border_top_left_radius=border_radius,
                         border_top_right_radius=border_radius)

        pygame.draw.rect(self.surface, theme.board_border.light, (
            BOARD_START_X - BORDER_RADIUS,
            BOARD_START_Y + BOARD_HEIGHT // 2,
            BOARD_WIDTH + BORDER_RADIUS * 2,
            BOARD_HEIGHT // 2 + BORDER_RADIUS), border_bottom_left_radius=border_radius,
                         border_bottom_right_radius=border_radius)

    def show_turn_indicator(self):
        color = self.config.theme.turn_indicator.light

        pygame.draw.rect(self.surface, color,
                         self.turn_indicator_white if self.next_player == "black" else self.turn_indicator_black,
                         border_radius=BORDER_RADIUS * 2)

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
                        pygame.draw.rect(self.surface, color,
                                         (col * SQSIZE + BOARD_START_X, row * SQSIZE + BOARD_START_Y, SQSIZE, SQSIZE),
                                         **kwargs)
                        continue

                pygame.draw.rect(self.surface, color,
                                 (col * SQSIZE + BOARD_START_X, row * SQSIZE + BOARD_START_Y, SQSIZE, SQSIZE))

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

            pygame.draw.rect(self.surface, self.config.theme.turn_indicator.light, rect, width=SQSIZE // 20)

    def darken_area(self, shadow_surface, dest=(0, 0), size=(100, 100)):

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
        self.board.timer.add_increment()
        self.board.timer.active_player = self.next_player

    def set_hover(self, row, col):
        pass
        # self.hovered_square = self.board.squares[row][col]

    def change_theme(self, random=False, dir=1):
        if random:
            self.config.randomize_theme()
        else:
            self.config.change_theme(dir)
        self.update_colors()


    def update_colors(self):
        theme = self.config.theme
        self.checkmate_prompt = Button(
            text="",
            width=200,
            height=150,
            pos=(SCR_WIDTH // 2, SCR_HEIGHT // 2),
            action=lambda: print("hello")
        )

        self.turn_indicator_black = pygame.Rect(
            BOARD_START_X - BORDER_RADIUS * 2,
            BOARD_START_Y + BOARD_WIDTH / 2 + BORDER_RADIUS * 2,
            BOARD_WIDTH + BORDER_RADIUS * 2 * 2,
            BOARD_WIDTH / 2 - BORDER_RADIUS * 2)

        self.turn_indicator_white = pygame.Rect(
            BOARD_START_X - BORDER_RADIUS * 2,
            BOARD_START_Y - BORDER_RADIUS * 2,
            BOARD_WIDTH + BORDER_RADIUS * 2 * 2,
            BOARD_WIDTH / 2 - BORDER_RADIUS * 2)

        self.darkened_color = tuple(i * (0.95 - theme.shadow_opacity) for i in theme.bg.dark)
        self.darker_color = tuple(i * (0.9 - theme.shadow_opacity) for i in theme.bg.dark)


        self.exit_button = Button(
            image=exit_image,
            width=40,
            height=40,
            pos=(SCR_WIDTH - 40, 0),
            hover_color=theme.turn_indicator.light,
            action=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
        )
        self.minimize_button = Button(
            image=minimize_image,
            width=40,
            height=40,
            pos=(SCR_WIDTH - 80, 0),
            hover_color=theme.turn_indicator.light,
            action=lambda: pygame.event.post(pygame.event.Event(pygame.display.iconify()))
        )

        self.time_control_btns = [Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="Play",
            text_color=theme.bg.light,
            width=(SIDEBAR_WIDTH // 4 * 3 + SETTING_BTN_WIDTH) - (SIDEBAR_WIDTH // 4),
            # Tedious arithmetic just to get the correct width..
            height=40,
            bg_color=theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (2 + 6 * 4)),
            action=lambda: self.main.set_should_reset(),
            border_radius=BORDER_RADIUS // 2
        ),  Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="1 min",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=(SIDEBAR_WIDTH // 4 - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * 1.5),
            action=lambda: self.prepare_clock(1, 0),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="1 | 1",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 2) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * 1.5),
            action=lambda: self.prepare_clock(1, 1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="2 | 1",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 3) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * 1.5),
            action=lambda: self.prepare_clock(2, 1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="3 min",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=(SIDEBAR_WIDTH // 4 - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (1.5 + 6)),
            action=lambda: self.prepare_clock(3, 0),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="3 | 2",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 2) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (1.5 + 6)),
            action=lambda: self.prepare_clock(3, 2),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="5 min",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 3) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (1.5 + 6)),
            action=lambda: self.prepare_clock(5,0),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="10 min",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (1.5 + 6 * 2)),
            action=lambda: self.prepare_clock(10, 0),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="15 | 10",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 2) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (1.5 + 6 * 2)),
            action=lambda: self.prepare_clock(15, 10),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="30 min",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 3) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * (1.5 + 6 * 2)),
            action=lambda: self.prepare_clock(30, 0),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="-",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH // 2.1,
            height=30,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 3) - SETTING_BTN_WIDTH // 2, 118 + 52 + BORDER_RADIUS * (2 + 6 * 3)),
            action=lambda: self.increment_clock("incr", -1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="+",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH // 2.1,
            height=30,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 3) + (SETTING_BTN_WIDTH // 2 - SETTING_BTN_WIDTH // 2.1), 118 + 52 + BORDER_RADIUS * (2 + 6 * 3)),
            action=lambda: self.increment_clock("incr", 1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="-",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH // 2.1,
            height=30,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 2) - SETTING_BTN_WIDTH // 2, 118 + 52 + BORDER_RADIUS * (2 + 6 * 3)),
            action=lambda: self.increment_clock("secs", -1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="+",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH // 2.1,
            height=30,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 2) + (SETTING_BTN_WIDTH // 2 - SETTING_BTN_WIDTH // 2.1), 118 + 52 + BORDER_RADIUS * (2 + 6 * 3)),
            action=lambda: self.increment_clock("secs", 1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="-",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH // 2.1,
            height=30,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + 52 + BORDER_RADIUS * (2 + 6 * 3)),
            action=lambda: self.increment_clock("mins", -1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="+",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH // 2.1,
            height=30,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 ) + (SETTING_BTN_WIDTH // 2 - SETTING_BTN_WIDTH // 2.1), 118 + 52 + BORDER_RADIUS * (2 + 6 * 3)),
            action=lambda: self.increment_clock("mins", 1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="Prev",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + (SCR_HEIGHT - 40) // 2),
            action=lambda: self.change_theme(False, -1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="Next",
            text_color=theme.bg.light,
            width=SETTING_BTN_WIDTH,
            height=40,
            bg_color= theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4 * 3) - SETTING_BTN_WIDTH // 2.1, 118 + (SCR_HEIGHT - 40) // 2),
            action=lambda: self.change_theme(False, 1),
            border_radius=BORDER_RADIUS // 2
        ), Button(
            hover_color=theme.turn_indicator.light,
            font=self.font_corbel,
            text="Randomize",
            text_color=theme.bg.light,
            width=(SIDEBAR_WIDTH // 4 * 3 + SETTING_BTN_WIDTH) - (SIDEBAR_WIDTH // 4),
            # Tedious arithmetic just to get the correct width..
            height=40,
            bg_color=theme.bg.dark,
            pos=((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2.1, 118 + 52 + (SCR_HEIGHT - 40) // 2),
            action=lambda: self.change_theme(True),
            border_radius=BORDER_RADIUS // 2)
        ]

        self.reset_button = Button(
            font=self.font_segoe,
            text="New Game",
            bg_color=theme.bg.dark,
            text_color = theme.bg.light,
            hover_color = theme.turn_indicator.light,
            width=200,
            height=75,
            pos = (SCR_WIDTH // 2 - 200 // 2, SCR_HEIGHT // 2 + (SQSIZE - 75) / 2 + SQSIZE // 2),
            action =lambda: self.main.set_should_reset(),
            border_radius = BORDER_RADIUS
        )

        self.game_end_rect = pygame.Rect(SCR_WIDTH // 2 - 200, SCR_HEIGHT // 2 - 150, 400, 300)

        self.bullet_icon = pygame.image.load("../assets/vectors/bullet.svg")
        self.bullet_icon_rect = self.bullet_icon.get_rect()
        self.bullet_icon_rect.center = ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118)
        self.blitz_icon = pygame.image.load("../assets/vectors/blitz.svg")
        self.blitz_icon_rect = self.blitz_icon.get_rect()
        self.blitz_icon_rect.center = ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * 6)
        self.rapid_icon = pygame.image.load("../assets/vectors/rapid.svg")
        self.rapid_icon_rect = self.rapid_icon.get_rect()
        self.rapid_icon_rect.center = ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * 6 * 2)
        self.custom_icon = pygame.image.load("../assets/vectors/custom.svg")
        self.custom_icon_rect = self.custom_icon.get_rect()
        self.custom_icon_rect.center = ((SIDEBAR_WIDTH // 4) - SETTING_BTN_WIDTH // 2, 118 + BORDER_RADIUS * 6 * 3)

        self.bg_rect = pygame.Rect(0, 0, SCR_WIDTH, SCR_HEIGHT)
        self.top_bar = pygame.Rect(0, 0, SCR_WIDTH, 40)

        self.black_timer = pygame.Rect((SCR_WIDTH - SQSIZE) // 2, BOARD_START_Y - (BORDER_RADIUS * 3), SQSIZE,
                                       BORDER_RADIUS * 3)
        self.white_timer = pygame.Rect((SCR_WIDTH - SQSIZE) // 2, BOARD_START_Y + BOARD_HEIGHT, SQSIZE,
                                       BORDER_RADIUS * 3)

        self.left_sidebar = pygame.Rect(0, 40, SIDEBAR_WIDTH, SCR_HEIGHT - 40)
        self.right_sidebar = pygame.Rect(SCR_WIDTH - SIDEBAR_WIDTH, 40, SIDEBAR_WIDTH, SCR_HEIGHT - 40)

    def reset_timer(self):

        # self.__init__(self.surface, self.init_time_mins, self.inc_time_secs)

        # Reset and start the timer
        self.board.timer.reset()
        self.board.timer.start("white")

    def remove_promote_buttons(self):
        for button in self.promotion_buttons:
            button.remove_button()

    def prepare_clock(self, init_time_mins, inc_time_secs):
        self.init_time_mins = init_time_mins
        self.inc_time_secs = inc_time_secs

    def increment_clock(self, value, increment):
        if value == "mins":
            self.init_time_mins += increment
            print(self.init_time_mins)
        elif value == "secs":
            self.init_time_mins += increment / 60
        elif value == "incr":
            self.inc_time_secs += increment
        self.prepare_clock(self.init_time_mins, self.inc_time_secs)
