from imports import *

FPS = 60
clock = pygame.time.Clock()
size = width, height = 500, 600

background_color = (158, 255, 224)

screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)


def write_game_data_in_file(game):
    text = ''
    text += f'money={game.money}\n'
    text += f'money_level={game.money_level}\n'
    text += f'milk={game.milk}\n'
    text += f'milk_level={game.milk_level}\n'
    text += f'auto_click={game.auto_click}\n'
    text += f'auto_sell={game.auto_sell}\n'
    with open('gamedata.txt', mode='w') as file:
        file.write(text)


def terminate():
    """Выход из приложения"""
    try:
        from windows.game import game
        write_game_data_in_file(game)
    finally:
        pygame.quit()
        pygame.mixer.quit()
        pygame.font.quit()
        sys.exit()


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
