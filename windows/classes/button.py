import pygame


class Text:
    def __init__(self, text: str, color: tuple[int, int, int] = (0, 0, 0)):
        self.font = pygame.font.SysFont('Times New Roman', 24)
        self.text = text
        self.color = color

    def draw(self, x, y):
        from values import screen
        text = self.font.render(self.text, False, self.color)
        screen.blit(text, (x, y))


class Button:
    def __init__(self,
                 text: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color_text: tuple[int, int, int] = (0, 0, 0)):

        self.font = pygame.font.Font(None, 32)
        self.text = text
        self.color_text = color_text

        self.x = x  # левый верхний угол
        self.y = y  # левый верхний угол
        self.width = width
        self.height = height
        self.color = (240, 108, 108)
        self.color_on_mouse = (255, 123, 123)
        self.mouse_on_button = False

    def draw(self, x, y):
        from values import screen
        self.check_mouse(x, y)
        border_radius = 15
        if self.mouse_on_button:
            pygame.draw.rect(screen, self.color_on_mouse,
                             pygame.Rect(self.x, self.y, self.width, self.height),
                             0, border_radius)
        else:
            pygame.draw.rect(screen, self.color,
                             pygame.Rect(self.x, self.y, self.width, self.height),
                             0, border_radius)

        text = self.font.render(self.text, False, self.color_text)
        screen.blit(text, (self.x + 10, self.y + 15))

    def check_mouse(self, x, y):
        if self.x <= x <= self.x + self.width and\
                self.y <= y <= self.y + self.height:
            self.mouse_on_button = True
            return True
        self.mouse_on_button = False
        return False
