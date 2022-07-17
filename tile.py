import pygame
pygame.font.init()

# GLOBAL CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

tile_font = pygame.font.SysFont("Arial", 20)

class Tile:
    """
    Represents a single tile of Sudoku board and manages tile state.
    """

    # CLASS VARIABLES
    rows = 9
    cols = 9
    padding = 20 # pixels

    def __init__(self, value, row, col, width, height, board, window):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.board = board
        self.window = window
        self.size = int((self.width - (2 * Tile.padding)) / 9)
        self.temp = 0 # temporary value typed in by user before they submit a tile.
        self.selected = False
        # Keep track of if algorithm has reached this tile through backtracking
        self.backtrack = False
        # If a tile's value is correct, it should no longer be able to be modified.
        self.is_immutable = True if self.board[self.row][self.col] == self.value and self.value != 0 else False
    
    def draw_tile(self, color):
        """
        Draws tile to pygame window.
        :param color: tuple
        :return: None
        """
        x_pos = (self.col * self.size) + Tile.padding
        y_pos = (self.row * self.size) + Tile.padding

        background = pygame.Surface((self.size - 4, self.size - 4))
        background.fill((WHITE))
        self.window.blit(background, (x_pos + 2, y_pos + 2))

        # If tile is selected, change background color
        if self.selected and not self.is_immutable:
            background = pygame.Surface((self.size, self.size))
            background.fill((0, 0, 200))
            background.set_alpha(150)
            self.window.blit(background, (x_pos, y_pos))  

        # If tile's value is not 0, draw it on the board
        if self.value != 0 or self.temp != 0:
            if self.temp != 0:
                tile_text = tile_font.render(str(self.temp), 1, color)
            else:
                tile_text = tile_font.render(str(self.value), 1, color)

            # Dynamically center text within tile
            self.window.blit(tile_text, 
                                ((x_pos + (self.size / 2 - tile_text.get_width() / 2)), 
                                (y_pos + (self.size / 2 - tile_text.get_height() / 2))))

    def draw_border(self):
        """
        Draws tile border during solution algorithm visualization.
        """

        x_pos = (self.col * self.size) + Tile.padding
        y_pos = (self.row * self.size) + Tile.padding

        if not self.backtrack:
            color = GREEN
        else:
            color = RED
        
        # Top border
        pygame.draw.line(self.window, color, (x_pos, y_pos), (x_pos + self.size - 2, y_pos), 2)
        # Right border
        pygame.draw.line(self.window, color, (x_pos + self.size - 2, y_pos), (x_pos + self.size - 2, y_pos + self.size - 2), 2)
        # Bottom border
        pygame.draw.line(self.window, color, (x_pos + self.size - 2, y_pos + self.size - 2), (x_pos, y_pos + self.size - 2), 2)
        # Left border
        pygame.draw.line(self.window, color, (x_pos, y_pos + self.size - 2), (x_pos, y_pos), 2)
    
    def set_val(self, val):
        self.value = val
    
    def set_temp_val(self, temp_val):
        self.temp = temp_val

