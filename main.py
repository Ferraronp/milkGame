from values import *
from windows.game import show_game_window

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    try:
        show_game_window()
    finally:
        terminate()
