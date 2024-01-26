import pygame.sprite

from values import *


class Catapult(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_group):
        super().__init__(sprite_group)
        self.x = x
        self.y = y
        image_name = "img/settings/catapult.png"
        size = (50, 50)
        self.image = pygame.transform.scale(load_image(image_name), size)
        self.orig = self.image
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.angle = 0
        self.update_image()

    def update_image(self):
        image_name = "img/settings/catapult.png"
        size = (50, 50)
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


running_settings = True


class Ball:
    def __init__(self, x, y, u, angle):
        self.x = x
        self.y = y
        self.delta_x = x
        self.delta_y = y
        self.u = u
        self.g = 10
        self.maxy = 100
        self.angle = angle * 3.14 / 180

    def update_coord_by_tick(self, ticks):
        from math import sin, cos
        t = ticks / 6
        if self.y != self.maxy:
            self.x = self.u * cos(self.angle) * t + self.delta_x
            self.y = self.u * sin(self.angle) * t + (self.g * (t ** 2)) / 2 + self.delta_y
            self.y = min(self.y, self.maxy)
            if self.y == self.maxy:
                return int((self.x - 160) / (463 - 160) * 100)
        return -1

    def draw(self):
        pygame.draw.circle(screen, 'Black', (self.x, self.y), 3)


def close_window():
    global running_settings
    running_settings = False


def write_settings(settings: dict):
    text = ''
    for setting in settings:
        text += f'{setting}={settings[setting]}\n'
    with open('settings.txt', mode='w') as file:
        file.write(text)


def get_settings():
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
        settings['music'] = 'music/fon.mp3'
    return settings


def show_settings_window():
    from windows.classes.button import Button
    global running_settings
    running_settings = True
    buttons_width = 150

    font = pygame.font.Font(None, 30)

    settings = get_settings()

    start_game_button = (Button('Назад', 330, 500, buttons_width, 50),
                         close_window)
    buttons = [start_game_button]

    change_music_settings_button = Button('', 20, 150, 20, 20, border_radius=0, delete_text=False)
    change_music_settings_button.color_of_toggled = (0, 0, 0)
    button_text = font.render("Я не справился с настройкой звука", 1, 'Black')

    fon_music_button = (Button('Боевая', 50, 310, buttons_width, 50), 'music/fon.mp3')
    chipichipi_music_button = (Button('Чипи-чипи', 50, 370, buttons_width, 50), 'music/chipichipi.mp3')
    dymok_music_button = (Button('Дымок', 50, 430, buttons_width, 50), 'music/dymok.mp3')
    music_buttons = [fon_music_button, chipichipi_music_button, dymok_music_button]

    settings_sprite_group = pygame.sprite.Group()
    catapult = Catapult(20, 60, settings_sprite_group)
    ball = Ball(settings['volume'] / 100 * (463 - 100) + 160, 100, 10, 0)

    mouse_x, mouse_y = 0, 0

    fonmusic = pygame.mixer.Sound(settings['music'])
    fonmusic.set_volume(settings['volume'] / 100)
    fonmusic.play(50000)

    catapult_pressed = False

    other_music_settings = False
    x, y = 20 + settings['volume'] / 100 * 460, 200
    deltax = 0
    drawing = False
    ticks_for_catapult = 0
    ticks_for_ball = 0
    angle = 0
    textvolume = font.render("Volume ", 1, 'Black')
    while running_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fonmusic.stop()
                close_window()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for button, func in buttons:
                    if button.check_mouse(mouse_x, mouse_y):
                        fonmusic.stop()
                        click = pygame.mixer.Sound('music/click.mp3')
                        click.set_volume(0.1)
                        click.play()
                        func()
                if catapult.rect.collidepoint(mouse_x, mouse_y):
                    catapult_pressed = True
                    ticks_for_catapult = 0
                if change_music_settings_button.check_mouse(mouse_x, mouse_y):
                    change_music_settings_button.toggled = True
                    other_music_settings = True
                for button, music in music_buttons:
                    if button.check_mouse(mouse_x, mouse_y):
                        settings['music'] = music
                        fonmusic.stop()
                        fonmusic = pygame.mixer.Sound(music)
                        fonmusic.set_volume(settings['volume'] / 100)
                        fonmusic.play(50000)
                        write_settings(settings)
                if x - 20 <= event.pos[0] <= x + 40 and \
                        y <= event.pos[1] <= y + 100 and \
                        other_music_settings:
                    drawing = True
                    deltax = event.pos[0] - x
            if event.type == pygame.MOUSEBUTTONUP:
                if catapult_pressed:
                    ticks_for_ball = 0
                    ball = Ball(45, 85, 63.25, angle=-angle)
                catapult_pressed = False
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if drawing:
                    if event.pos[0] - deltax < 20:
                        settings['volume'] = 0
                        write_settings(settings)
                        x = 20
                    elif 460 < event.pos[0] - deltax:
                        settings['volume'] = 100
                        write_settings(settings)
                        x = 460
                    else:
                        x = event.pos[0] - deltax
                        settings['volume'] = int((x - 20) / 440 * 100)
                        write_settings(settings)
                    fonmusic.set_volume(settings['volume'] / 100)

        if catapult_pressed:
            angle = min(45, ticks_for_catapult / 60 * 7)
            catapult.image = pygame.transform.rotate(catapult.orig, int(angle))
            catapult.rect = catapult.image.get_rect(center=catapult.rect.center)
        ticks_for_catapult += 1

        pygame.draw.rect(screen, background_color,
                         pygame.Rect(0, 0, 1000000, 1000000))
        if other_music_settings:
            pygame.draw.rect(screen, "black",
                             (19, 199, 462, 102), width=1)
            pygame.draw.rect(screen, "blue",
                             (x, y, 20, 100))
        change_music_settings_button.draw(mouse_x, mouse_y)

        rect = textvolume.get_rect()
        rect.x += 20
        rect.y += 20
        screen.blit(textvolume, rect)
        text = font.render(str(settings['volume']) + " %", 1, 'Black')
        rect.x += rect.width
        screen.blit(text, rect)
        screen.blit(button_text, button_text.get_rect().move(50, 150))

        settings_sprite_group.draw(screen)
        volume = ball.update_coord_by_tick(ticks_for_ball)
        if volume != -1:
            settings['volume'] = volume
            fonmusic.set_volume(settings['volume'] / 100)
            write_settings(settings)
        ball.draw()
        pygame.draw.line(screen, 'Black', (160, 100), (463, 100))
        ticks_for_ball += 1
        for button, _ in buttons + music_buttons:
            button.draw(mouse_x, mouse_y)

        pygame.display.flip()
        clock.tick(FPS)
