import pygame

class Button:
    def __init__(self, surface, text, bg, fg, x, y, width, height):
        self.surface = surface
        self.bg = bg
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        font = pygame.font.SysFont("Arial", height//2, "bold")
        self.label = font.render(text, True, fg)

    def draw(self):
        pygame.draw.rect(self.surface, self.bg, self.rect)
        self.surface.blit(self.label, (self.x + self.width*0.25,
                                       self.y + self.height*0.25))
