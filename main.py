from values import *
from windows.game import show_game_window
'''import webbrowser
webbrowser.open('http:/youtube.com', new=2)'''

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    show_game_window()
    terminate()

# TODO: добавить кнопки в меню
# TODO: добавить кнопки в игре и сделать спрайты для смены
# TODO: сделать настройки
# TODO: сделать магазин(добавить кнопки)
