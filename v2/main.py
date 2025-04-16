import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from soundmanager import SoundManager
from pygame.locals import *
# Adapted from https://www.youtube.com/watch?v=OpL0Gcfn4B4
class Main:

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 1, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.WINDOWMINIMIZED | DOUBLEBUF)
        pygame.display.set_caption("Chess")
        Game.SCR_WIDTH = self.screen.get_width()
        Game.SCR_HEIGHT = self.screen.get_height()
        self.game = Game(self.screen)
        self.shadow_surface = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()



    def mainloop(self):
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        shadow_surface = self.shadow_surface

        while 1:
            game.show_gui()
            game.show_turn_indicator()
            game.show_board_misc()
            game.show_bg()
            game.show_last_move()
            game.show_coords()
            game.show_hover()
            game.show_moves(shadow_surface)
            game.show_pieces()
            game.show_promotion(shadow_surface)
            game.show_checkmate(shadow_surface)

            self.clock.tick()
            print(self.clock.get_fps())

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
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEMOTION:  # Mouse motion
                    dragger.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:  # Release click

                    if dragger.dragging:
                        dragger.undrag_piece()
                        (release_row, release_col), is_valid = dragger.grid_coords()
                        initial = Square(dragger.initial_row, dragger.initial_col, board)
                        final = Square(release_row, release_col, board)
                        move = Move(initial, final)

                        game.show_hover()
                        if board.valid_move(dragger.piece, move): # Is the move valid
                            # Normal capture
                            # print("valid")
                            board.check_promote(dragger.piece, final)
                            board.was_last_move_capture = board.squares[release_row][release_col].has_piece()
                            board.move(dragger.piece, move)

                            game.next_turn()


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

            # game.randomize_theme()

            pygame.display.update()


main = Main()


main.mainloop()
