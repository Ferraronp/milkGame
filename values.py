from imports import *

main_menu_sprites = pygame.sprite.Group()
shop_menu_sprites = pygame.sprite.Group()
settings_menu_sprites = pygame.sprite.Group()

FPS = 60
clock = pygame.time.Clock()
size = width, height = 500, 600

background_color = (158, 255, 224)

screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)


def terminate():
    """Выход из приложения"""
    pygame.quit()
    pygame.mixer.quit()
    pygame.font.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Загрузка изображения из папки data"""
    # fullname = os.path.join('data', name)
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
