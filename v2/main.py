import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from soundmanager import SoundManager
from pygame.locals import *

class Main:

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 1, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | DOUBLEBUF)
        pygame.display.set_caption("Chess")
        Game.SCR_WIDTH = self.screen.get_width()
        Game.SCR_HEIGHT = self.screen.get_height()
        self.game = Game(self.screen)
        self.shadow_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

    exit_button = Button(
        image=exit_image,
        width=40,
        height=40,
        pos=(SCR_WIDTH - 40, 0),
        bg_color=(255, 0, 0),
        hover_color=(255, 255, 255),
        action=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
    )
    minimize_button = Button(
        image=minimize_image,
        width=40,
        height=40,
        pos=(SCR_WIDTH - 80, 0),
        bg_color=(255, 0, 0),
        hover_color=RED,
        action=lambda: pygame.event.post(pygame.event.Event(pygame.display.iconify()))
    )

    def mainloop(self):
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        shadow_surface = self.shadow_surface

        while 1:
            game.show_gui()
            game.show_bg()
            game.show_last_move()
            game.show_coords()
            game.show_hover()
            game.show_moves(shadow_surface)
            game.show_pieces()
            game.show_promotion(shadow_surface)

            # clock.tick(144)
            # print(clock.get_fps())

            for event in pygame.event.get():
                hover_coords, is_hover_valid = dragger.grid_coords(
                    event.pos if event.type == pygame.MOUSEMOTION else None)
                if is_hover_valid:
                    game.set_hover(hover_coords[0], hover_coords[1])
                else:
                    game.set_hover(None, None)  # Clear hover if outside board

                if event.type == pygame.MOUSEBUTTONDOWN:  # Detect click
                    (clicked_row, clicked_col), is_valid = dragger.grid_coords(event.pos)
                    if not is_valid:
                        continue

                    if board.squares[clicked_row][clicked_col].has_piece() and not board.pending_promotion:
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                elif event.type == pygame.MOUSEMOTION:  # Mouse motion
                    dragger.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:  # Release click

                    if dragger.dragging:
                        dragger.undrag_piece()
                        (release_row, release_col), is_valid = dragger.grid_coords()
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(release_row, release_col)
                        move = Move(initial, final)

                        game.show_hover()
                        if board.valid_move(dragger.piece, move): # Is the move valid
                            # Normal capture
                            # print("valid")

                            capture = board.squares[release_row][release_col].has_piece()
                            board.check_promote(dragger.piece, move.final)
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)
                            game.next_turn()
                            SoundManager().play("capture" if capture else "move")


                elif event.type == pygame.KEYDOWN: # Change theme hotkey
                    if event.key == pygame.K_t:
                        game.change_theme()
                    if event.key == pygame.K_g:
                        game.randomize_theme()
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT: # Quit app
                    pygame.quit()
                    sys.exit()

            self.exit_button.draw(self.screen)
            self.exit_button.handle_event()
            self.minimize_button.draw(self.screen)
            self.minimize_button.handle_event()

            pygame.display.update()


main = Main()


main.mainloop()
