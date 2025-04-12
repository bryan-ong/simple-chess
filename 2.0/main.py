import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from soundmanager import SoundManager

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Chess")
        Game.SCR_WIDTH = self.screen.get_width()
        Game.SCR_HEIGHT = self.screen.get_height()
        self.game = Game(self.screen)
        self.shadow_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)

    def mainloop(self):
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        shadow_surface = self.shadow_surface

        while True:
            game.show_gui()
            game.show_bg()
            game.show_last_move()
            game.show_coords()
            game.show_hover()
            game.show_moves(shadow_surface)
            game.show_pieces()
            game.show_promotion(shadow_surface)

            for event in pygame.event.get():
                game.set_hover(dragger.grid_coords()[0], dragger.grid_coords()[1])

                if event.type == pygame.MOUSEBUTTONDOWN:  # Detect click
                    clicked_row, clicked_col = dragger.grid_coords()
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
                        release_row, release_col = dragger.grid_coords()

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
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT: # Quit app
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()


main.mainloop()
