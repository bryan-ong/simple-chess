import time

import pygame.time


class ChessTimer:
    def __init__(self, initial_time_minutes=10, increment_seconds=0):
        self.initial_time_mili = initial_time_minutes * 60 * 1000
        self.increment_mili = increment_seconds * 1000
        self.reset()
        self.clock = pygame.time.Clock

    def reset(self):
        self.white_time = self.initial_time_mili
        self.black_time = self.initial_time_mili
        self.last_update_time = pygame.time.get_ticks()
        self.active_player = None
        self.paused = True

    def start(self, player):
        if self.paused and self.active_player: # Can only start if it's paused first, and also there is a player to tick the timer from
            self._update_time()
        self.active_player = player
        self.last_update_time = pygame.time.get_ticks()
        self.paused = False

    def pause(self):
        if not self.paused and self.active_player: # Extra resiliency here too
            self._update_time()

        self.paused = True


    def _update_time(self):
        if not self.active_player or self.paused: # Don't tick if no player, extra resiliency
            return

        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_update_time

        if self.active_player == "white":
            self.white_time -= delta_time
        else:
            self.black_time -= delta_time
        # This will be called once per frame, however is not frame dependent since we are using get_ticks()
        self.last_update_time = current_time

    def add_increment(self):
        # In case the players want to play those increment time modes, bullet? or blitz I can't remember
        if self.active_player == "white":
            self.white_time += self.increment_mili
        else:
            self.black_time += self.increment_mili

    def get_formatted_time(self, player):
        # Gets the formatted time for a player, minute:second:millisecond format

        if player == 'white':
            ms = max(0, self.white_time)
        else:
            ms = max(0, self.black_time)

        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        milliseconds = ms % 1000
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}" # Return as stripped double

    def get_simple_formatted_time(self, player):
        # Same thing but simpler, for easier display on screen
        if player == 'white':
            seconds = max(0, self.white_time) // 1000
        else:
            seconds = max(0, self.black_time) // 1000

        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def is_timeout(self):
        return self.white_time <= 0 or self.black_time <= 0

    def get_loser(self):
        if self.white_time <= 0:
            return "white"
        elif self.black_time <= 0:
            return "black"
        return None

    def update(self, clock):
        self._update_time()
        self.clock.tick(clock)