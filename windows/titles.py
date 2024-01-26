import pygame.sprite

from values import *

running_titles = True


def close_window():
    global running_titles
    running_titles = False


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word for word in text.splitlines()]  # 2D array where each row is a list of words.
    mx_word = max(words, key=len)
    words = ['{s:{c}>{n}}'.format(s=word, n=len(mx_word), c=' ') for word in text.splitlines()]

    max_width, max_height = surface.get_size()

    word_surface = font.render(mx_word, 0, color)
    word_width, word_height = word_surface.get_size()

    x, y = pos
    x = (max_width - word_width) / 2
    for word in words:
        word_surface = font.render(word, 0, color)
        word_width, word_height = word_surface.get_size()
        surface.blit(word_surface, (x, y))
        y += word_height


def show_titles_window():
    from windows.classes.button import Button

    global running_titles
    running_titles = True

    back_button = (Button('Назад', 350, 500, 100, 50),
                   close_window)
    buttons = [back_button]

    font = pygame.font.SysFont('Lexend', 50)
    text = "Разработчик\nFerraronp\n\nХудожник\nПсихомерзость"

    mouse_x, mouse_y = 0, 0

    while running_titles:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running_titles = False
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
        blit_text(screen, text, (150, 20), font)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    show_titles_window()
    terminate()
