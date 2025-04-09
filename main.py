# https://www.youtube.com/watch?v=X-e0jk4I938 Guided using this tutorial
# https://www.youtube.com/watch?v=8SzTzvrWaAA
# https://python-forum.io/thread-25114.html
# Assets from https://sharechess.github.io/
# And many other forums...
import pygame
import pygame.gfxdraw
import sys
from pygame import MOUSEBUTTONDOWN
from pygame._sdl2 import Window
from typer.colors import WHITE

# COLORS
GREEN = (105, 146, 62)
DARK_GREEN = (78, 120, 55)
GRAY = (75, 72, 71)
DARK_GRAY = (44, 43, 41)
RED = (255, 100, 100)
SELECT_CIRCLE_COLOR = (125, 125, 125)
DARKER_GRAY = (25, 25, 25)

class Button:
    def __init__(self, text="", image=None, width=None, height=None, pos=(0, 0), text_color=DARK_GRAY,
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
        self.font = font_bold
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
font = pygame.font.Font("segoeui.ttf", 12)
font_bold = pygame.font.Font("segoeuib.ttf", 20)
big_font = pygame.font.Font("segoeuib.ttf", 32)
timer = pygame.time.Clock()
fps = 60
grid_size = 100
piece_scale = (grid_size * 0.9, grid_size * 0.9)
piece_scale_small = (piece_scale[0] * 0.5, piece_scale[0] * 0.5)
board_grid_size = 8
board_size = board_grid_size * grid_size
board_start_x = (screen.get_width() - board_size) // 2
board_start_y = (screen.get_height() - board_size) // 2
border_radius = 15
# shadow_surface = screen
# shadow_surface.fill(pygame.Color(0, 0, 0))
# shadow_mask = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
# shadow_mask.fill(pygame.Color(0, 0, 0, 0))

capture_area_width_factor = 0.6

# Game variables and assets
close_img = pygame.transform.scale(
    pygame.image.load("assets/images/closebtn.png"),
    (20, 20)
)

capture_sound = pygame.mixer.Sound("assets/sounds/capture.mp3")
move_sound = pygame.mixer.Sound("assets/sounds/move-self.mp3")

white_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]


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
black_queen = pygame.transform.scale(pygame.image.load("assets/images/qb.png"), piece_scale)
black_queen_small = pygame.transform.scale(pygame.image.load("assets/images/qb.png"), piece_scale_small)

white_queen = pygame.transform.scale(pygame.image.load("assets/images/qw.png"), piece_scale)
white_queen_small = pygame.transform.scale(pygame.image.load("assets/images/qw.png"), piece_scale_small)

black_king = pygame.transform.scale(pygame.image.load("assets/images/kb.png"), piece_scale)
black_king_small = pygame.transform.scale(pygame.image.load("assets/images/kb.png"), piece_scale_small)

white_king = pygame.transform.scale(pygame.image.load("assets/images/kw.png"), piece_scale)
white_king_small = pygame.transform.scale(pygame.image.load("assets/images/kw.png"), piece_scale_small)

black_bishop = pygame.transform.scale(pygame.image.load("assets/images/bb.png"), piece_scale)
black_bishop_small = pygame.transform.scale(pygame.image.load("assets/images/bb.png"), piece_scale_small)

white_bishop = pygame.transform.scale(pygame.image.load("assets/images/bw.png"), piece_scale)
white_bishop_small = pygame.transform.scale(pygame.image.load("assets/images/bw.png"), piece_scale_small)

black_rook = pygame.transform.scale(pygame.image.load("assets/images/rb.png"), piece_scale)
black_rook_small = pygame.transform.scale(pygame.image.load("assets/images/rb.png"), piece_scale_small)

white_rook = pygame.transform.scale(pygame.image.load("assets/images/rw.png"), piece_scale)
white_rook_small = pygame.transform.scale(pygame.image.load("assets/images/rw.png"), piece_scale_small)

black_knight = pygame.transform.scale(pygame.image.load("assets/images/nb.png"), piece_scale)
black_knight_small = pygame.transform.scale(pygame.image.load("assets/images/nb.png"), piece_scale_small)

white_knight = pygame.transform.scale(pygame.image.load("assets/images/nw.png"), piece_scale)
white_knight_small = pygame.transform.scale(pygame.image.load("assets/images/nw.png"), piece_scale_small)

black_pawn = pygame.transform.scale(pygame.image.load("assets/images/pb.png"), piece_scale)
black_pawn_small = pygame.transform.scale(pygame.image.load("assets/images/pb.png"), piece_scale_small)

white_pawn = pygame.transform.scale(pygame.image.load("assets/images/pw.png"), piece_scale)
white_pawn_small = pygame.transform.scale(pygame.image.load("assets/images/pw.png"), piece_scale_small)

white_assets = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_assets_small = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small,
                      white_bishop_small]
black_assets = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
black_assets_small = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small,
                      black_bishop_small]

piece_list = ["pawn", "queen", "king", "knight", "rook", "bishop"]



top_bar = pygame.Rect(
    0, 0,
    screen.get_width(),
    40
)

bottom_bar = pygame.Rect(
    0, screen.get_height() - 40,
    screen.get_width(), 40
)

white_captured_rect = pygame.Rect(
    screen.get_width() - board_size / (2 / capture_area_width_factor), board_start_y,
    board_size / 2, board_size / 2
)

black_captured_rect = pygame.Rect(
    screen.get_width() - board_size / (2 / capture_area_width_factor), board_start_y + board_size / 2,
    board_size / 2, board_size / 2
)

captured_rect = pygame.Rect(
    screen.get_width() - board_size / (2 / capture_area_width_factor) - border_radius, board_start_y - border_radius,
    board_size / 2 + border_radius, board_size + border_radius * 2
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

    # Turn indicator
    if turn_step <= 1:
        pygame.draw.rect(screen, RED, (
            board_start_x - border_radius * 2,
            board_start_y - border_radius * 2,
            board_size + border_radius * 2 * 2,
            board_size / 2), border_radius=border_radius * 2)
    else:
        pygame.draw.rect(screen, RED, (
            board_start_x - border_radius * 2,
            board_start_y + board_size / 2 + border_radius * 2,
            board_size + border_radius * 2 * 2,
            board_size / 2), border_radius=border_radius * 2)

    # Replicate shadow effect, would use blur() but that is in pygame-ce not pygame
    pygame.draw.rect(screen, DARKER_GRAY, (
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

    text_surface = big_font.render(status_text[turn_step], True, DARK_GRAY if turn_step >= 2 else WHITE)

    screen.blit(text_surface, text_surface.get_rect(center=bottom_bar.center))  # Render instruction text

    # Timer rects
    x_offset = board_start_x + board_size / 2 - grid_size / 4 - grid_size / 2

    pygame.draw.rect(screen, WHITE, (
        x_offset, board_start_y - 40 - border_radius,
        grid_size * 1.5, 40,
    ), border_top_left_radius=border_radius, border_top_right_radius=border_radius)

    pygame.draw.rect(screen, DARK_GRAY, (
        x_offset, board_start_y + board_size + border_radius,
        grid_size * 1.5, 40,
    ), border_bottom_left_radius=border_radius, border_bottom_right_radius=border_radius)

def draw_valid_moves(moves):
    if turn_step <= 1:
        for i in range(len(moves)):
            if (moves[i][0], moves[i][1]) in black_locations:
                pygame.draw.circle(screen, SELECT_CIRCLE_COLOR, (
                    board_start_x + moves[i][0] * grid_size + grid_size / 2,
                    board_start_y + moves[i][1] * grid_size + grid_size / 2,
                ), grid_size * 0.45, width=10)
            else:
                pygame.draw.circle(screen, SELECT_CIRCLE_COLOR, (
                    board_start_x + moves[i][0] * grid_size + grid_size / 2,
                    board_start_y + moves[i][1] * grid_size + grid_size / 2,
                ), 15)
    elif turn_step >= 2:
        for i in range(len(moves)):
            if (moves[i][0], moves[i][1]) in white_locations:
                pygame.draw.circle(screen, SELECT_CIRCLE_COLOR, (
                    board_start_x + moves[i][0] * grid_size + grid_size / 2,
                    board_start_y + moves[i][1] * grid_size + grid_size / 2,
                ), grid_size * 0.45, width=10)
            else:
                pygame.draw.circle(screen, SELECT_CIRCLE_COLOR, (
                    board_start_x + moves[i][0] * grid_size + grid_size / 2,
                    board_start_y + moves[i][1] * grid_size + grid_size / 2,
                ), 15)


# Draw misc elements
def draw_misc():
    pygame.draw.rect(screen, GREEN, top_bar)
    pygame.draw.rect(screen, DARK_GREEN, bottom_bar)
    pygame.draw.rect(screen, DARK_GREEN, captured_rect,
                     border_bottom_left_radius=border_radius,
                     border_top_left_radius=border_radius)
    pygame.draw.rect(screen, WHITE, white_captured_rect,
                     border_top_left_radius=border_radius)
    pygame.draw.rect(screen, DARK_GRAY, black_captured_rect,
                     border_bottom_left_radius=border_radius)


# Draw pieces onto board
def draw_pieces():
    radius = grid_size * 0.4
    centered_pos = (grid_size - piece_scale[0]) / 2
    for i in range(len(white_pieces)):
        if turn_step <= 1:
            if selection == i:
                # Added translucency rendering for the shadow, but it looked ugly, reverting to solid color
                pygame.draw.circle(screen, SELECT_CIRCLE_COLOR, (  # Draw selection circle
                    board_start_x + white_locations[i][0] * grid_size + grid_size / 2,
                    board_start_y + white_locations[i][1] * grid_size + grid_size / 2,
                ), radius)

        index = piece_list.index(white_pieces[i])
        screen.blit(white_assets[index], (  # Draw white pieces
            board_start_x + white_locations[i][0] * grid_size + centered_pos,
            board_start_y + white_locations[i][1] * grid_size + centered_pos))

    for i in range(len(black_pieces)):
        if turn_step >= 2:
            if selection == i:
                pygame.draw.circle(screen, SELECT_CIRCLE_COLOR, (  # Draw selection circle
                    board_start_x + black_locations[i][0] * grid_size + grid_size / 2,
                    board_start_y + black_locations[i][1] * grid_size + grid_size / 2,
                ), radius)

        index = piece_list.index(black_pieces[i])
        screen.blit(black_assets[index], (  # Draw black pieces
            board_start_x + black_locations[i][0] * grid_size + centered_pos,
            board_start_y + black_locations[i][1] * grid_size + centered_pos))


def draw_captured_pieces():
    # Calculation for offset
    x_offset = screen.get_width() - board_size / (2 / capture_area_width_factor) + 30
    center_y = board_start_y + board_size / 2
    white_counts = {"pawn": 0, "knight": 0, "bishop": 0, "rook": 0, "queen": 0, "king": 0}
    black_counts = {"pawn": 0, "knight": 0, "bishop": 0, "rook": 0, "queen": 0, "king": 0}

    for piece in captured_pieces_white:
        black_counts[piece] += 1  # White captures black pieces

    for piece in captured_pieces_black:
        white_counts[piece] += 1  # Black captures white pieces

    piece_spacing = 15
    vertical_gap = 10
    distance_from_middle = 50
    piece_height = piece_scale_small[1]

    for i, piece_type in enumerate(["pawn", "knight", "bishop", "rook", "queen", "king"]):
        # if piece_type == "king":
        #     # Will add game over handling here
        #     break

        count_black = black_counts[piece_type]

        white_y = center_y + vertical_gap + (i * (piece_height + vertical_gap)) + distance_from_middle
        black_y = center_y - vertical_gap - (i * (piece_height + vertical_gap)) - piece_height - distance_from_middle

        if count_black > 0:

            # Draw piece icons
            for j in range(count_black):
                index = piece_list.index(piece_type)
                piece_x = x_offset - piece_spacing * (j + 1) + grid_size * 1.25
                screen.blit(black_assets_small[index], (piece_x, black_y))

            # Draw count black text
            text_surf = font_bold.render(str(count_black), True, DARK_GRAY)
            text_y = black_y + piece_height / 2 - text_surf.get_height() / 2
            screen.blit(text_surf, (x_offset + grid_size * 1.25 + 50, text_y))

        count_white = white_counts[piece_type]
        if count_white > 0:
            # Draw the piece icons
            for j in range(count_white):
                index = piece_list.index(piece_type)
                piece_x = x_offset - piece_spacing * (j + 1) + grid_size * 1.25
                screen.blit(white_assets_small[index], (piece_x, white_y))

            # Draw text counter for white
            text_surf = font_bold.render(str(count_white), True, WHITE)
            text_y = white_y + piece_height / 2 - text_surf.get_height() / 2
            screen.blit(text_surf, (x_offset + grid_size * 1.25 + 50, text_y))


# Function to check valid options for alive pieces
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == "pawn":
            moves_list = check_pawns(location, turn)
        elif piece == "knight":
            moves_list = check_knights(location, turn)
        elif piece == "rook":
            moves_list = check_rooks(location, turn, 8)
        elif piece == "bishop":
            moves_list = check_bishops(location, turn, 8)
        elif piece == "king":
            moves_list = check_kings(location, turn)
        elif piece == "queen":
            moves_list = check_queens(location, turn)
        all_moves_list.append(moves_list)

    return all_moves_list


def check_pawns(location, turn):
    moves_list = []
    x = location[0]
    y = location[1]
    options = [(x, y + 1), (x, y + 2), (x + 1, y + 1), (x - 1, y + 1), (x, y - 1), (x, y - 2),
               (x + 1, y - 1), (x - 1, y - 1)]

    if turn == "white":
        if options[0] not in white_locations and options[0] not in black_locations and 0 <= y < board_grid_size:
            moves_list.append(options[0])
            if (options[1] not in white_locations and
                    options[1] not in black_locations and
                    y == 1):  # Only first move of pawn can go 2 squares
                moves_list.append(options[1])


        if options[2] in black_locations:
            moves_list.append(options[2])

        if options[3] in black_locations:
            moves_list.append(options[3])

    else:
        if options[4] not in black_locations and options[4] not in white_locations and 0 <= y < board_grid_size:
            moves_list.append(options[4])

        if (options[5] not in black_locations and
                options[5] not in white_locations and
                y == 6):  # Only first move of pawn can go 2 squares
            moves_list.append(options[5])

        if options[6] in white_locations:
            moves_list.append(options[6])

        if options[7] in white_locations:
            moves_list.append(options[7])

    return moves_list


def check_knights(location, turn):
    moves_list = []
    x = location[0]
    y = location[1]
    # All valid knight moves
    options = [(x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2), (x - 1, y - 2), (x - 2, y - 1),
               (x - 2, y + 1), (x - 1, y + 2)]

    # I realized that the tutorial's code was extremely inefficient and this is much more compact, will try implement this for check_pawns()
    for i in range(len(options)):
        # Check collision with all pieces
        if 0 <= options[i][0] < board_grid_size and 0 <= options[i][1] < board_grid_size:  # Limit to game board
            if options[i] not in white_locations and options[i] not in black_locations:
                moves_list.append(options[i])
            if turn == "white":
                # Check capturing moves for opponent
                if options[i] in black_locations:
                    moves_list.append(options[i])

            else:
                if options[i] in white_locations:
                    moves_list.append(options[i])

    return moves_list

def check_rooks(location, turn, range):
    moves_list = []

    if turn == "white":
        enemy_list = black_locations
        ally_list = white_locations
    else:
        enemy_list = white_locations
        ally_list = black_locations

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up as pygame reads y downwards
    x = location[0]
    y = location[1]


    for dx, dy in directions:
        distance = 1
        while True:
            current_loc = (x + dx * distance, y + dy * distance)

            if distance > range:
                break

            if not (0 <= current_loc[0] < board_grid_size and 0 <= current_loc[1] < board_grid_size): # If move isn't inside board, break
                break

            if current_loc not in enemy_list and current_loc not in ally_list: # Check for empty spot and increment distance and continue
                moves_list.append(current_loc)
                distance += 1
                continue

            if current_loc in enemy_list: # If found enemy then break
                moves_list.append(current_loc)

            break

    return moves_list

def check_bishops(location, turn, range):
    moves_list = []

    if turn == "white":
        enemy_list = black_locations
        ally_list = white_locations
    else:
        enemy_list = white_locations
        ally_list = black_locations

    directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # Bottom-right, Bottom-left, Top-left, Top-right as pygame reads y downwards
    x = location[0]
    y = location[1]


    for dx, dy in directions:
        distance = 1
        while True:
            current_loc = (x + dx * distance, y + dy * distance)

            if distance > range:
                break

            if not (0 <= current_loc[0] < board_grid_size and 0 <= current_loc[1] < board_grid_size): # If move isn't inside board, break
                break

            if current_loc not in enemy_list and current_loc not in ally_list: # Check for empty spot and increment distance and continue
                moves_list.append(current_loc)
                distance += 1
                continue

            if current_loc in enemy_list: # If found enemy then break
                moves_list.append(current_loc)

            break

    return moves_list

def check_kings(location, turn):
    # Added range parameter for more reusability and flexibility
    return check_bishops(location, turn, 1) + check_rooks(location, turn, 1)

def check_queens(location, turn):
    return check_bishops(location, turn, 8) + check_rooks(location, turn, 8)

# Gets just the valid moves for the currently selected piece
def filter_valid_moves():
    if turn_step <= 1:
        options_list = white_options
    else:
        options_list = black_options

    valid_options = options_list[selection]

    return valid_options


# Main game loop
black_options = check_options(black_pieces, black_locations, "black")
white_options = check_options(white_pieces, white_locations, "white")
run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    timer.tick(fps)
    screen.fill(GRAY)

    draw_misc()
    draw_board()

    if selection != 100:
        valid_moves = filter_valid_moves()
        draw_valid_moves(valid_moves)

    draw_pieces()
    draw_captured_pieces()
    # Event handler

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x_coord = (event.pos[0] - board_start_x) // grid_size
            y_coord = (event.pos[1] - board_start_y) // grid_size
            click_coords = (x_coord, y_coord)  # Convert to index on grid
            if turn_step <= 1:  # Whites turn
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0: turn_step = 1

                if click_coords in valid_moves and selection != 100:  # Clicked on valid move square
                    move_sound.play()
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)  # Get index of black piece that was clicked on
                        capture_sound.play()
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                    black_options = check_options(black_pieces, black_locations, "black")
                    white_options = check_options(white_pieces, white_locations, "white")

                    turn_step = 2  # Increment turn
                    selection = 100  # Deselect
                    valid_moves = []  # Clear valid moves for further recalculation

            if turn_step >= 2:  # Whites turn
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2: turn_step = 3

                if click_coords in valid_moves and selection != 100:  # Clicked on valid move square
                    move_sound.play()
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)  # Get index of black piece that was clicked on
                        capture_sound.play()
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)

                    black_options = check_options(black_pieces, black_locations, "black")
                    white_options = check_options(white_pieces, white_locations, "white")

                    turn_step = 0  # Increment turn
                    selection = 100  # Deselect
                    valid_moves = []  # Clear valid moves for further recalculation

        exit_button.handle_event(event)

    exit_button.check_hover(mouse_pos)

    exit_button.draw(screen)

    pygame.display.flip()
pygame.quit()
sys.exit()
