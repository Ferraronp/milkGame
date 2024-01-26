import pygame.sprite

from values import *
from windows.game import game

running_shop = True


def close_window():
    global running_shop
    running_shop = False


def show_shop_window():
    from windows.classes.button import Button
    global running_shop

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

    running_shop = True

    next_money_level = min(game.money_level + 1, len(game.money_levels) - 1)
    text = f'{game.money_levels[next_money_level]["description"]} за {game.money_levels[next_money_level]["price"]}$'
    update_money_button = (Button(text, 50, 120, 1, 50),
                           game.update_money)
    update_money_button[0].width = game.money_levels[next_money_level]["button_width"]

    next_milk_level = min(game.milk_level + 1, len(game.milk_levels) - 1)
    update_milk_button = (Button(f'{game.milk_levels[next_milk_level]["description"]} за {game.milk_levels[next_milk_level]["price"]}$',
                                 50, 180, 1, 50),
                          game.update_milk)
    update_milk_button[0].width = game.milk_levels[next_milk_level]["button_width"]

    update_auto_click_button = (Button(f'Купить автоклик за {game.auto_click_price}$',
                                       50, 240, 290, 50),
                                game.buy_auto_click)
    update_auto_sell_button = (Button(f'Купить автопродажу за {game.auto_sell_price}$',
                                      50, 300, 330, 50),
                               game.buy_auto_sell)
    update_auto_sell_button[0].toggled = True

    exit_button = (Button('Назад', 50, 360, 200, 50),
                   close_window)
    buttons = [update_money_button, update_milk_button, update_auto_click_button, update_auto_sell_button, exit_button]
    if game.money_level + 1 == len(game.money_levels):
        update_money_button[0].toggled = True
    if game.milk_level + 1 == len(game.milk_levels):
        update_milk_button[0].toggled = True
    if game.milk_level + 1 == len(game.milk_levels) and not game.auto_sell:
        update_auto_sell_button[0].toggled = False

    mouse_x, mouse_y = 0, 0

    while running_shop:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running_shop = False
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

                        next_money_level = min(game.money_level + 1, len(game.money_levels) - 1)
                        text = f'{game.money_levels[next_money_level]["description"]} за {game.money_levels[next_money_level]["price"]}$'
                        update_money_button[0].text = text
                        update_money_button[0].width = game.money_levels[next_money_level]["button_width"]
                        if game.money_level + 1 == len(game.money_levels):
                            update_money_button[0].toggled = True

                        next_milk_level = min(game.milk_level + 1, len(game.milk_levels) - 1)
                        update_milk_button[0].text = f'{game.milk_levels[next_milk_level]["description"]} за {game.milk_levels[next_milk_level]["price"]}$'
                        update_milk_button[0].width = game.milk_levels[next_milk_level]["button_width"]
                        if game.milk_level + 1 == len(game.milk_levels):
                            update_milk_button[0].toggled = True

                        update_auto_click_button[0].text = f'Купить автоклик за {game.auto_click_price}$'

                        if game.milk_level + 1 == len(game.milk_levels):
                            update_auto_sell_button[0].toggled = False

                        if game.auto_sell:
                            update_auto_sell_button[0].toggled = True

        pygame.draw.rect(screen, background_color,
                         pygame.Rect(0, 0, 1000000, 1000000))
        for button, _ in buttons:
            button.draw(mouse_x, mouse_y)
        pygame.display.flip()
        clock.tick(FPS)
