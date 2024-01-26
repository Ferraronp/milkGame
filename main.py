from values import *

try:
    file_path = 'gamedata.txt'
    open(file_path, 'x')
except FileExistsError:
    print('File already exists')
try:
    file_path = 'settings.txt'
    open(file_path, 'x')
except FileExistsError:
    print('File already exists')

from windows.game import show_game_window

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    try:
        show_game_window()
    finally:
        terminate()
