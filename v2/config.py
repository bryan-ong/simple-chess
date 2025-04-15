
import pygame
import os
from const import *
from sound import Sound
from theme import Theme
from random import randint
from random import uniform
from random import getrandbits

class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', SQSIZE // 5, bold=True)



        self.move_sound = Sound(
            os.path.join(SOUNDS_DIR, 'move.mp3'))
        self.capture_sound = Sound(
            os.path.join(SOUNDS_DIR, 'capture.mp3'))
        self.check_sound = Sound(
            os.path.join(SOUNDS_DIR, 'check.mp3'))
        self.castle_sound = Sound(
            os.path.join(SOUNDS_DIR, 'castle.mp3'))
        self.promote_sound = Sound(
            os.path.join(SOUNDS_DIR, 'promote.mp3'))
        self.checkmate_sound = Sound(
            os.path.join(SOUNDS_DIR, 'checkmate.mp3'))


    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((240,236,212), "black", (245,246,130), (119, 154, 88), (185,202,67), rounded=False)
        brown = Theme((235, 209, 166), "black", (245, 234, 100),(165, 117, 80), (209, 185, 59), rounded=True)
        blue = Theme((229, 228, 200), "black",(123, 187, 227) ,(60, 95, 135), (43, 119, 191), rounded=False)
        gray = Theme((120, 119, 118),"white",(99, 126, 143), (86, 85, 84),(82, 102, 128), shadow_opacity=0.25, rounded=True)
        red = Theme(RED, RED, RED)

        self.themes = [green, brown, blue, gray, red]

    def randomize_theme(self):
        colors = [randint(0, 255) for _ in range(7 * 3)] # Generates 7 tuples of 3
        rgb_tuples = [tuple(colors[i:i + 3]) for i in range(0, len(colors), 3)]
        # This will split the flat color array into tuples of 3, 0:3 then 3:6 then 3:9 and so on and so forth

        random = Theme(rgb_tuples[0], rgb_tuples[1], rgb_tuples[2], rgb_tuples[3], rgb_tuples[4], rgb_tuples[5], rgb_tuples[6], shadow_opacity=uniform(0.15, 0.35), rounded=bool(getrandbits(1)),)

        self.theme = random