# import os
# from sound import Sound
# from theme import Theme
# from const import *
# 
# class Config:
#     def __init__(self):
#         self.themes = []
# 
#         self._add_themes()
#         self.idx = 0
#         self.theme = self.themes[self.idx]
# 
#         self.move_sound = Sound(
#             os.path.join("assets/sounds/move.mp3")
#         )
#         self.capture_sound = Sound(
#             os.path.join("assets/sounds/capture.mp3")
#         )
# 
#     def change_theme(self):
#         self.idx += 1
#         self.idx %= len(self.themes)  # Allows wrapping of themes, scrolling
#         self.theme = self.themes[self.idx]
# 

import pygame
import os
from const import *
from sound import Sound
from theme import Theme

class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', SQSIZE // 5, bold=True)

        self.move_sound = Sound(
            os.path.join('assets/sounds/move.mp3'))
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.mp3'))
        self.check_sound = Sound(
            os.path.join('assets/sounds/check.mp3'))
        self.castle_sound = Sound(
            os.path.join('assets/sounds/castle.mp3'))
        self.promote_sound = Sound(
            os.path.join('assets/sounds/promote.mp3'))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((240,236,212), "black", (245,246,130), (119, 154, 88), (185,202,67))
        brown = Theme((235, 209, 166), "black", (245, 234, 100),(165, 117, 80), (209, 185, 59))
        blue = Theme((229, 228, 200), "black",(123, 187, 227) ,(60, 95, 135), (43, 119, 191))
        gray = Theme((120, 119, 118),"white",(99, 126, 143), (86, 85, 84),(82, 102, 128), shadow_opacity=0.25)

        self.themes = [green, brown, blue, gray]