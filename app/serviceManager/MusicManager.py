from pygame import mixer
from .ExceptionManager import *


def play_music(path):
    try:
        mixer.init()
        mixer.music.load(path)
        mixer.music.play()
    except Exception:
        print_exception_info("ERROR OCCURRED WHEN PLAYING SOUND", Exception)