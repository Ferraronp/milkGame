import pygame.sprite

from values import *
running_menu = True


def close_window():
    global running_menu
    running_menu = False


def show_menu_window():
    from windows.classes.button import Button
    from windows.settings import show_settings_window
    from windows.titles import show_titles_window
    import webbrowser

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

    global running_menu
    running_menu = True

    buttons_width = 200
    start_game_button = (Button('Начать игру', 50, 60, buttons_width, 50),
                         close_window)
    settings_button = (Button('Настройки', 50, 120, buttons_width, 50),
                       show_settings_window)
    titles_button = (Button('Титры', 50, 180, buttons_width, 50),
                     show_titles_window)
    donation_button = (Button('Пожертвования', 50, 240, buttons_width, 50),
                       lambda: webbrowser.open('https://www.donationalerts.com/r/ferraronp', new=2))
    exit_button = (Button('Выйти', 50, 300, buttons_width, 50),
                   terminate)
    buttons = [start_game_button, settings_button, titles_button, donation_button, exit_button]

    mouse_x, mouse_y = 0, 0

    while running_menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running_menu = False
                terminate()
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button, func in buttons:
                    if button.check_mouse(x, y):
                        click = pygame.mixer.Sound('music/click.mp3')
                        click.set_volume(0.1)
                        click.play()
                        func()
        pygame.draw.rect(screen, background_color,
                         pygame.Rect(0, 0, 1000000, 1000000))
        for button, _ in buttons:
            button.draw(mouse_x, mouse_y)
        pygame.display.flip()
        clock.tick(FPS)
