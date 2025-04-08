# https://www.youtube.com/watch?v=X-e0jk4I938 Guided using this tutorial
# https://www.youtube.com/watch?v=8SzTzvrWaAA
# https://python-forum.io/thread-25114.html
# And many other forums...
import pygame, sys
import pygame.gfxdraw
from pygame._sdl2 import Window

# COLORS
GREEN = (105, 146, 62)
DARK_GREEN = (78, 120, 55)
GRAY = (75, 72, 71)
DARK_GRAY = (44, 43, 41)
RED = (255, 100, 100)

class Button:
    def __init__(self, text="", image=None, width=None, height=None, pos=(0,0), text_color=DARK_GRAY, bg_color=DARK_GREEN, hover_color=GREEN, action=None):
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
        self.font = font
        self.text_surf = self.font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # Initialization
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        if not self.image or self.is_hovered:
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos) and self.action:
                self.action()
                return True
            return False

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Simple Chess")
Window.from_display_module().maximize()
font = pygame.font.Font("segoeui.ttf", 20)
big_font = pygame.font.Font("segoeuib.ttf", 50)
timer = pygame.time.Clock()
fps = 60
piece_scale = (80, 80)
piece_scale_small = (45, 45)
pawn_scale = (60, 60)
pawn_scale_small = (30, 30)
grid_size = 100
board_grid_size = 8
board_size = board_grid_size * grid_size
board_start_x = (screen.get_width() - board_size) // 2
board_start_y = (screen.get_height() - board_size) // 2
border_radius = 15
# Game variables and assets
white_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

# Top Left = (0, 0)
# Bottom Right = (0, 0)

black_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []
# 0 - White's turn, no selection
# 1 - White's turn, piece selected
# 2 - Black's turn, no selection
# 3 - Black's turn, piece selected

turn_step = 0
selection = 100
valid_moves = []
# Load assets for pieces
black_queen = pygame.transform.scale(pygame.image.load("assets/images/qb.svg"), piece_scale)
black_queen_small = pygame.transform.scale(pygame.image.load("assets/images/qb.svg"), piece_scale_small)

white_queen = pygame.transform.scale(pygame.image.load("assets/images/qw.svg"), piece_scale)
white_queen_small = pygame.transform.scale(pygame.image.load("assets/images/qw.svg"), piece_scale_small)

black_king = pygame.transform.scale(pygame.image.load("assets/images/kb.svg"), piece_scale)
black_king_small = pygame.transform.scale(pygame.image.load("assets/images/kb.svg"), piece_scale_small)

white_king = pygame.transform.scale(pygame.image.load("assets/images/kw.svg"), piece_scale)
white_king_small = pygame.transform.scale(pygame.image.load("assets/images/kw.svg"), piece_scale_small)

black_bishop = pygame.transform.scale(pygame.image.load("assets/images/bb.svg"), piece_scale)
black_bishop_small = pygame.transform.scale(pygame.image.load("assets/images/bb.svg"), piece_scale_small)

white_bishop = pygame.transform.scale(pygame.image.load("assets/images/bw.svg"), piece_scale)
white_bishop_small = pygame.transform.scale(pygame.image.load("assets/images/bw.svg"), piece_scale_small)

black_rook = pygame.transform.scale(pygame.image.load("assets/images/rb.svg"), piece_scale)
black_rook_small = pygame.transform.scale(pygame.image.load("assets/images/rb.svg"), piece_scale_small)

white_rook = pygame.transform.scale(pygame.image.load("assets/images/rw.svg"), piece_scale)
white_rook_small = pygame.transform.scale(pygame.image.load("assets/images/rw.svg"), piece_scale_small)

black_knight = pygame.transform.scale(pygame.image.load("assets/images/nb.svg"), piece_scale)
black_knight_small = pygame.transform.scale(pygame.image.load("assets/images/nb.svg"), piece_scale_small)

white_knight = pygame.transform.scale(pygame.image.load("assets/images/nw.svg"), piece_scale)
white_knight_small = pygame.transform.scale(pygame.image.load("assets/images/nw.svg"), piece_scale_small)

black_pawn = pygame.transform.scale(pygame.image.load("assets/images/kb.svg"), pawn_scale)
black_pawn_small = pygame.transform.scale(pygame.image.load("assets/images/kb.svg"), pawn_scale_small)

white_pawn = pygame.transform.scale(pygame.image.load("assets/images/kw.svg"), pawn_scale)
white_pawn_small = pygame.transform.scale(pygame.image.load("assets/images/kw.svg"), pawn_scale_small)

white_assets = [white_pawn, white_queen, white_king, white_rook, white_bishop]
white_assets_small = [white_pawn_small, white_queen_small, white_king_small, white_rook_small, white_bishop_small]
black_assets = [black_pawn, black_queen, black_king, black_rook, black_bishop]
black_assets_small = [black_pawn_small, black_queen_small, black_king_small, black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

close_img = pygame.transform.scale(
    pygame.image.load("assets/images/closebtn.png"),
    (20, 20)
)

top_bar = pygame.Rect(
    0, 0,
    screen.get_width(),
    40
)

bottom_bar = pygame.Rect(
    0, screen.get_height() - grid_size,
    screen.get_width(), screen.get_height() - (board_start_y + board_size)
)
exit_button = Button(
    image=close_img,
    width=40,
    height=40,
    pos=(screen.get_width() - 40, 0),
    hover_color=RED,
    action=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
)

# Check variables / flashing counter

# Draw main game board
def draw_board():
    # Replicate shadow effect, would use blur() but that is in pygame-ce not pygame
    pygame.draw.rect(screen, DARK_GRAY, (
        board_start_x - border_radius,
        board_start_y - border_radius,
        board_size + border_radius * 2,
        board_size + border_radius * 2), border_radius=border_radius)

    for row in range(board_grid_size):
        for col in range(board_grid_size):
            if (row + col) % 2 == 0:
                color = "white"
            else:
                color = "dark gray"

            x = board_start_x + col * grid_size
            y = board_start_y + row * grid_size

            if row == 0 and col == 0:
                pygame.draw.rect(screen, color, (x, y, grid_size, grid_size), border_top_left_radius=border_radius)
            elif row == 0 and col == 7:
                pygame.draw.rect(screen, color, (x, y, grid_size, grid_size), border_top_right_radius=border_radius)
            elif row == 7 and col == 0:
                pygame.draw.rect(screen, color, (x, y, grid_size, grid_size), border_bottom_left_radius=border_radius)
            elif row == 7 and col == 7:
                pygame.draw.rect(screen, color, (x, y, grid_size, grid_size), border_bottom_right_radius=border_radius)
            else:
                pygame.draw.rect(screen, color, (x, y, grid_size, grid_size))

    status_text = ["White: Select a Piece to Move", "White: Select a Destination",
                   "Black: Select a Piece to Move", "Black: Select a Destination"]

    text_surface = big_font.render(status_text[turn_step], True, DARK_GRAY)

    screen.blit(text_surface, text_surface.get_rect(center=bottom_bar.center)) # Render instruction text

def draw_misc():

    pygame.draw.rect(screen, GREEN, top_bar)
    pygame.draw.rect(screen, DARK_GREEN,bottom_bar)

    pygame.draw.rect(screen, "black", (
        board_start_x + grid_size / 2, board_start_y - 40 - border_radius,
        grid_size * 1.5, 40,
        ), border_top_left_radius=border_radius, border_top_right_radius=border_radius)

    pygame.draw.rect(screen, "white", (
        board_start_x + board_size - grid_size / 2 - grid_size * 1.5, board_start_y - 40 - border_radius,
        grid_size * 1.5, 40,
    ), border_top_left_radius=border_radius, border_top_right_radius=border_radius)

def draw_elements():
    draw_misc()
    draw_board()
    # draw_white_area()
    # draw_black_area()


# Main game loop
run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    timer.tick(fps)
    screen.fill(GRAY)

    draw_elements()
    # Event handler
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False

        exit_button.handle_event(events)



    exit_button.check_hover(mouse_pos)

    exit_button.draw(screen)

    pygame.display.flip()
pygame.quit()
sys.exit()
