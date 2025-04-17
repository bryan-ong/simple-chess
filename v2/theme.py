from color import Color
from const import *
class Theme:
    def __init__(self,
                 light_bg, moves, light_trace, dark_board_border,
                 dark_bg=None, dark_trace=None,
                 turn_indicator=RED, light_board_border=None, rounded=False,
                 darken_scale=0.9, shadow_opacity=0.14):

        # Procedurally generated dark colors if dark colors were not specified
        self.bg = Color(light_bg, dark_bg if dark_bg is not None else tuple(i * (darken_scale - 0.2) for i in light_bg))
        self.trace = Color(light_trace, dark_trace if dark_trace is not None else tuple(i * darken_scale for i in light_trace))
        self.moves = Color(moves, moves)
        self.turn_indicator = Color(turn_indicator, turn_indicator)
        self.board_border = Color(light_board_border if light_board_border is not None else tuple(min(255, i * (20 * darken_scale)) for i in dark_board_border),
                                  (tuple(max(0, i * darken_scale / 3) for i in dark_board_border)))
        self.rounded = rounded
        self.shadow_opacity = shadow_opacity