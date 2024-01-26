import pygame.sprite

from values import *
from data import Game


def get_game_data_from_file() -> dict:
    game_data = dict()
    for line in open('gamedata.txt', mode='r').readlines():
        try:
            text = line.split('=')
            game_data[text[0]] = text[1].strip()
        except Exception:
            pass
    return game_data


global game
game = Game(**get_game_data_from_file())


class Clicker(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_group):
        super().__init__(sprite_group)
        self.x = x
        self.y = y
        self.image = None
        self.rect = None
        self.image_name = None
        self.size = (1, 1)
        self.update_image()

    def update_image(self):
        self.image_name = game.money_levels[game.money_level]['image']
        self.size = game.money_levels[game.money_level]['size']
        self.image = pygame.transform.scale(load_image(self.image_name), self.size)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def on_click(self):
        self.image = pygame.transform.scale(self.image, (self.size[0] - 5, self.size[1] - 5))
        self.rect = self.image.get_rect().move(self.x + 2, self.y + 2)
        game.update_milk_on_click()


class MilkLimits(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_group):
        super().__init__(sprite_group)
        self.x = x
        self.y = y
        self.image = None
        self.rect = None
        self.update_image()

    def update_image(self):
        image_name = game.milk_levels[game.milk_level]['image']
        size = game.milk_levels[game.milk_level]['size']
        self.image = pygame.transform.scale(load_image(image_name), size)
        self.rect = self.image.get_rect().move(self.x, self.y)


class Worker(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        super().__init__(sprite_group)
        self.x = 0
        self.y = 0
        self.image = None
        self.rect = None
        self.update_image()

    def update_image(self):
        image_name = game.milk_levels[game.milk_level]['worker_image']
        size = game.milk_levels[game.milk_level]['worker_image_size']
        self.x, self.y = game.milk_levels[game.milk_level]['xy_worker']
        self.image = pygame.transform.scale(load_image(image_name), size)
        self.rect = self.image.get_rect().move(self.x, self.y)


def get_settings_from_file() -> dict:
    settings = dict()
    for line in open('settings.txt', mode='r').readlines():
        try:
            text = line.split('=')
            settings[text[0]] = text[1].strip()
        except Exception:
            pass

    try:
        settings['volume'] = int(settings['volume'])
    except Exception:
        settings['volume'] = 10

    if 'music' not in settings:
        settings['music'] = 'music/chipichipi.mp3'
    return settings


def show_game_window():
    global game
    from windows.classes.button import Button
    from windows.menu import show_menu_window
    from windows.shop import show_shop_window

    show_menu_window()

    menu_button = (Button('Меню', 340, 500, 150, 50),
                   show_menu_window, True)
    shop_menu = (Button('Магазин', 40, 440, 230, 50),
                 show_shop_window, False)
    sell_button = (Button(f'Продать за {game.get_money_of_milk()}$', 40, 500, 230, 50),
                   game.sell_milk, False)
    buttons = [menu_button, shop_menu, sell_button]

    settings = get_settings_from_file()

    game_sprite_group = pygame.sprite.Group()
    clicker = Clicker(120, 5, game_sprite_group)
    milk_level = MilkLimits(50, 310, game_sprite_group)
    worker = Worker(game_sprite_group)

    font = pygame.font.Font(None, 30)

    running = True
    mouse_x, mouse_y = 0, 0

    fonmusic = pygame.mixer.music
    fonmusic.load(settings['music'])
    fonmusic.set_volume(settings['volume'] / 100)
    fonmusic.play(50000)

    ticks_for_clicker = -1
    ticks = 0

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fonmusic.pause()
                mouse_x, mouse_y = 0, 0
                show_menu_window()
                settings_new = get_settings_from_file()
                if settings != settings_new:
                    settings = settings_new
                    fonmusic.stop()
                    fonmusic.unload()
                    fonmusic.load(settings['music'])
                    fonmusic.set_volume(settings['volume'] / 100)
                    fonmusic.play(50000)
                fonmusic.unpause()
                for sprite in game_sprite_group:
                    sprite.update_image()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button, func, stop_music, *args in buttons:
                    if button.check_mouse(x, y):
                        if stop_music:
                            fonmusic.pause()
                        mouse_x, mouse_y = 0, 0
                        click = pygame.mixer.Sound('music/click.mp3')
                        click.set_volume(0.1)
                        click.play()
                        func()
                        if stop_music:
                            settings_new = get_settings_from_file()
                            if settings != settings_new:
                                settings = settings_new
                                fonmusic.stop()
                                fonmusic.unload()
                                fonmusic.load(settings['music'])
                                fonmusic.set_volume(settings['volume'] / 100)
                                fonmusic.play(50000)
                            fonmusic.unpause()
                        for sprite in game_sprite_group:
                            sprite.update_image()
                if clicker.rect.collidepoint(x, y):
                    click = pygame.mixer.Sound('music/click.mp3')
                    click.set_volume(0.05)
                    click.play()
                    clicker.on_click()
                    ticks_for_clicker = 5

        pygame.draw.rect(screen, background_color,
                         pygame.Rect(0, 0, 1000000, 1000000))

        sell_button[0].text = f'Продать за {game.get_money_of_milk()}$'
        for button, *args in buttons:
            button.draw(mouse_x, mouse_y)
        game_sprite_group.draw(screen)

        text = font.render(str(game.money) + ' $', 1, (191, 11, 70))
        rect = text.get_rect()
        rect.x += 20
        rect.y += 20
        ticks_for_clicker -= 1
        ticks += 1

        screen.blit(text, rect)
        if ticks_for_clicker == 0:
            clicker.update_image()
        if ticks % 61 == 0:
            game.update(1)
        pygame.display.flip()
        clock.tick(FPS)
