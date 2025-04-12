# sound_manager.py
class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._sounds = {}

    def set_config(self, config):
        self._sounds = {
            "capture": config.capture_sound,
            "check": config.check_sound,
            "castle": config.castle_sound,
            "promote": config.promote_sound,
            "move": config.move_sound,
        }


    def play(self, sound="move"):
        if sound in self._sounds:
            self._sounds[sound].play()
        else:
            self._sounds["move"].play()
