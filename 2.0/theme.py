from color import Color

class Theme:
    def __init__(self,
                 light_bg, moves, light_trace,
                 dark_bg=None, dark_trace=None,
                 darken_scale=0.9, shadow_opacity=0.14):

        # Procedurally generated dark colors if dark colors were not specified
        self.bg = Color(light_bg, dark_bg if dark_bg is not None else tuple(i * (darken_scale - 0.2) for i in light_bg))
        self.trace = Color(light_trace, dark_trace if dark_trace is not None else tuple(i * darken_scale for i in light_trace))
        self.moves = Color(moves, moves)
        self.shadow_opacity = shadow_opacity