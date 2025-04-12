import pygame
from const import *


class Button:
    def __init__(self, text="", font=None, image=None, width=None, height=None, pos=(0, 0), text_color=None,
                 bg_color=DARK_GREEN, hover_color=GREEN, action=None):
        self.image = image

        if width is None:
            width = image.get_width() if image else 100
        if height is None:
            height = image.get_height() if image else 100

        # Center image on button
        self.rect = pygame.Rect(pos, (width, height))
        if image:
            self.image_rect = image.get_rect(center=self.rect.center)

        # Text initialization
        self.text = text
        self.font = pygame.font.SysFont('monospace', 18, bold=True) if font is None else font
        self.text_surf = self.font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # Initialization
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        if not self.image or self.is_hovered or self.bg_color:
            pygame.draw.rect(surface, self.current_color, self.rect)

        if self.image:
            surface.blit(self.image, self.image_rect)

        if self.text:
            surface.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        # Check if hovered by comparing with mouse
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.bg_color
        return self.is_hovered

    def handle_event(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.action:
            if pygame.mouse.get_pressed()[0]: # Originally used pygame events but this is easier as we do not need to run it inside the event if statement, just the main loop for rendering
                self.action()
                return True
        return False

    def remove_button(self):
        del self
