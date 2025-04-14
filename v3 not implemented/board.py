from v2.player import Player
from square import Square

class Board:
    def __init__(self, size, game_mode="default"):
        self.cols = size(0)
        self.rows = size(1)

        self.game_mode = game_mode
        self.player_list = (Player("white"), Player("black"))
        self.player_count = len(self.player_list)
        self.current_player = self.player_list[0]
        self.squares = [[Square(row, col) for col in range(self.cols)] for row in range(self.rows)]