import pygame.mouse

from const import *

# https://python-forum.io/thread-25114.html
class Button:
    def __init__(self, text="", font=None, image=None, width=None, height=None, pos=(0, 0), text_color=(255, 0, 0),
                 bg_color=(0, 0, 0, 0), hover_color=(125, 25, 25), action=None):
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
        self.pressed = False

    def draw(self, surface):
        self.check_hover()
        # if not self.image or self.is_hovered:
        pygame.draw.rect(surface, self.current_color, self.rect)

        if self.image:
            surface.blit(self.image, self.image_rect)

        if self.text:
            surface.blit(self.text_surf, self.text_rect)


    def draw_and_handle(self, surface, remove_after=True):
        self.draw(surface)
        self.handle_click(remove_after)

    def check_hover(self):
        # Check if hovered by comparing with mouse
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.current_color = self.hover_color if self.is_hovered else self.bg_color
        return self.is_hovered

    def handle_click(self, remove_after=True):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Check if mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            if not mouse_pressed and self.pressed:
                if remove_after:
                    self.remove_button()
                self.action()
                self.pressed = False
                return
            elif mouse_pressed and not self.pressed:
                self.pressed = True
                print("pressed")
                return
        else:
            self.pressed = False
            return

    def remove_button(self):
        del self
