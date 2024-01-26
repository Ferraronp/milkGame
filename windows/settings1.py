import pygame.sprite
from values import *
running_settings = True


def close_window():
    global running_settings
    running_settings = False


def write_settings(settings: dict):
    text = ''
    for setting in settings:
        text += f'{setting}={settings[setting]}\n'
    with open('settings.txt', mode='w') as file:
        file.write(text)


def show_settings_window():
    from windows.classes.button import Button
    global running_settings
    running_settings = True
    buttons_width = 150

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

    start_game_button = (Button('Назад', 330, 500, buttons_width, 50),
                         close_window)
    buttons = [start_game_button]

    fon_music_button = (Button('Боевая', 50, 200, buttons_width, 50), 'music/fon.mp3')
    chipichipi_music_button = (Button('Чипи-чипи', 50, 260, buttons_width, 50), 'music/chipichipi.mp3')

    music_buttons = [fon_music_button, chipichipi_music_button]

    font = pygame.font.Font(None, 30)

    mouse_x, mouse_y = 0, 0

    fonmusic = pygame.mixer.Sound(settings['music'])
    fonmusic.set_volume(settings['volume'] / 100)
    fonmusic.play(50000)

    x, y = 20 + settings['volume'] / 100 * 460, 50
    deltax = 0
    drawing = False
    textvolume = font.render("Volume ", 1, pygame.Color('black'))
    while running_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fonmusic.stop()
                close_window()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, func in buttons:
                    if button.check_mouse(mouse_x, mouse_y):
                        fonmusic.stop()
                        click = pygame.mixer.Sound('music/click.mp3')
                        click.set_volume(0.1)
                        click.play()
                        func()
                for button, music in music_buttons:
                    if button.check_mouse(mouse_x, mouse_y):
                        settings['music'] = music
                        fonmusic.stop()
                        fonmusic = pygame.mixer.Sound(music)
                        fonmusic.set_volume(settings['volume'] / 100)
                        fonmusic.play(50000)
                        write_settings(settings)
                if x - 20 <= event.pos[0] <= x + 40 and \
                        y <= event.pos[1] <= y + 100:
                    drawing = True
                    deltax = event.pos[0] - x
            if event.type == pygame.MOUSEBUTTONUP:
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
        pygame.draw.rect(screen, background_color,
                         pygame.Rect(0, 0, 1000000, 1000000))

        pygame.draw.rect(screen, "black",
                         (19, 49, 462, 102), width=1)
        pygame.draw.rect(screen, "blue",
                         (x, y, 20, 100))
        rect = textvolume.get_rect()
        rect.x += 20
        rect.y += 20
        screen.blit(textvolume, rect)
        text = font.render(str(settings['volume']) + " %", 1, pygame.Color('black'))
        rect.x += rect.width
        screen.blit(text, rect)

        for button, _ in buttons + music_buttons:
            button.draw(mouse_x, mouse_y)

        pygame.display.flip()
        clock.tick(FPS)
