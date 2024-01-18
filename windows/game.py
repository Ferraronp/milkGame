import pygame.sprite

from values import *
from data import Game


class Clicker(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_group):
        super().__init__(sprite_group)
        self.x = x
        self.y = 10
        imagename = 'img/game/ketrin.jpg'
        self.image = pygame.transform.scale(load_image(imagename), (237, 320))
        self.rect = self.image.get_rect().move(self.x, self.y)


def show_game_window():
    from windows.classes.button import Button
    from windows.menu import show_menu_window

    game = Game()

    show_menu_window()

    menu_button = (Button('Меню', 340, 500, 150, 50),
                   show_menu_window)
    buttons = [menu_button]

    game_sprite_group = pygame.sprite.Group()
    Clicker(130, 10, game_sprite_group)

    running = True
    mouse_x, mouse_y = 0, 0

    pygame.draw.rect(screen, (255, 255, 255),
                     pygame.Rect(0, 0, 1000000, 1000000),
                     500)
    for button, _ in buttons:
        button.draw(mouse_x, mouse_y)
    pygame.draw.rect(screen, (255, 0, 255),
                     pygame.Rect(0, 1000, 1000000, 1000000),
                     500)
    game_sprite_group.draw(screen)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button, func in buttons:
                    if button.check_mouse(x, y):
                        mouse_x, mouse_y = 0, 0
                        func()
                for sprite in game_sprite_group:
                    if sprite.rect.collidepoint(x, y):
                        if type(sprite) == Clicker:
                            game.update_milk_on_click()
        pygame.draw.rect(screen, background_color,
                         pygame.Rect(0, 0, 1000000, 1000000))
        for button, _ in buttons:
            button.draw(mouse_x, mouse_y)
        game_sprite_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
