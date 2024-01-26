import pygame


class Button:
    def __init__(self,
                 text: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color_text: tuple[int, int, int] = (0, 0, 0),
                 border_radius=15,
                 delete_text=True):

        self.font = pygame.font.Font(None, 32)
        self.text = text
        self.color_text = color_text
        self.border_radius = border_radius
        self.delete_text = delete_text

        self.x = x  # левый верхний угол
        self.y = y  # левый верхний угол
        self.width = width
        self.height = height
        self.color = (240, 108, 108)
        self.color_on_mouse = (255, 123, 123)
        self.color_of_toggled = (220, 88, 88)
        self.toggled = False
        self.mouse_on_button = False

    def draw(self, x, y):
        from values import screen
        self.check_mouse(x, y)
        if self.toggled:
            color = self.color_of_toggled
        elif self.mouse_on_button:
            color = self.color_on_mouse
        else:
            color = self.color
        pygame.draw.rect(screen, color,
                         pygame.Rect(self.x, self.y, self.width, self.height),
                         0, self.border_radius)
        text = self.font.render(self.text, True, self.color_text)
        screen.blit(text, (self.x + 10, self.y + 15))
        if self.toggled and self.delete_text:
            pygame.draw.line(screen, (0, 0, 0), (self.x + 5, self.y + 25), (self.x - 10 + self.width, self.y + 25), 4)

    def check_mouse(self, x, y):
        if self.toggled:
            return False
        if self.x <= x <= self.x + self.width and\
                self.y <= y <= self.y + self.height:
            self.mouse_on_button = True
            return True
        self.mouse_on_button = False
        return False
