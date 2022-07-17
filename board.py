import random
import pygame
from board_options import board_options
from tile import Tile
pygame.font.init()

# GLOBAL CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

instruction_font_1 = pygame.font.SysFont("Arial", 15)
instruction_font_2 = pygame.font.SysFont("Arial", 12)

class Board:
    """
    Represents Sudoku board state and handles gameplay actions.
    """

    # CLASS VARIABLES
    padding = 20 # pixels

    def __init__(self, width, height, window):
        self.window = window
        self.board = random.choice(board_options)["board"] # Choose a random starting board from board_options
        self.solved_board = self.board["solved"]
        self.board = self.board["unsolved"]
        self.rows = 9
        self.cols = 9
        self.tiles = [[Tile(self.board[row][col], row, col, width, height, self.board, self.window) for col in range(self.cols)] for row in range(self.rows)]
        self.width = width
        self.height = height
        self.selected_tile = None
    
    def draw_board(self):
        """
        Draws board, tiles, and instruction text onto pygame window.
        """
        spacing = (self.width - (2 * Board.padding)) / 9

        # Make the lines separating the sub-grids thicker
        for i in range(self.rows + 1):
            if i % 3 == 0:
                thickness = 3
            else:
                thickness = 1

            # Draw horizontal grid lines
            pygame.draw.line(self.window, BLACK, 
                (Board.padding, i * spacing + Board.padding), 
                (self.width - Board.padding, i * spacing + Board.padding), thickness)
            # Draw vertical grid lines
            pygame.draw.line(self.window, BLACK, 
                (i * spacing + Board.padding, Board.padding), 
                (i * spacing + Board.padding, self.width - Board.padding), thickness)

        # Game instructions text
        instruction_text_1 = instruction_font_1.render("INSTRUCTIONS", 1, BLACK)
        instruction_text_2 = instruction_font_2.render("Click on a square to select it", 1, BLACK)
        instruction_text_3 = instruction_font_2.render("Type a number to insert it.", 1, BLACK)
        instruction_text_4 = instruction_font_2.render(
            "Press space to see the algorithm solve the board", 1, BLACK)
        # Dynamically center instruction text
        self.window.blit(instruction_text_1, 
            (self.width / 2 - (instruction_text_1.get_width() / 2), (self.width - 10)))
        self.window.blit(instruction_text_2, 
            (self.width / 2 - (instruction_text_2.get_width() / 2), (self.width + 20)))
        self.window.blit(instruction_text_3, 
            (self.width / 2 - (instruction_text_3.get_width() / 2), (self.width + 40)))
        self.window.blit(instruction_text_4, 
            (self.width / 2 - (instruction_text_4.get_width() / 2), (self.width + 60)))
        
        # Draw tiles on board
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw_tile(BLACK)
    
    def deselect_all_tiles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].selected = False
    
    def select_clicked_tile(self, mouse_pos):
        # Check if click was on game board
        if (mouse_pos[0] < self.width - Board.padding and mouse_pos[0] > Board.padding) \
            and (mouse_pos[1] < self.width - Board.padding and mouse_pos[1] > Board.padding):
            
            tile_size = self.width / 9

            # Calculate row and column of selected tile
            col = int(mouse_pos[0] // tile_size)
            row = int(mouse_pos[1] // tile_size)

            # Deselect current tile if already selected
            if self.tiles[row][col].selected == True:
                self.selected_tile = None
                self.tiles[row][col].selected = False
            else:
                self.deselect_all_tiles()
                
                # Select new tile
                if not self.tiles[row][col].is_immutable:
                    self.selected_tile = self.tiles[row][col]
                    self.selected_tile.selected = True
        else:
            # If user clicks outside of board, deselect current tile
            self.deselect_all_tiles()
            self.selected_tile = None                
            
    def solve(self):
        """
        Wrapper function for sudoku solver logic.
        """
        self.solve_partial_sudoku(0, 0)
    
    def solve_partial_sudoku(self, row, col):
        """
        Will solve partial sections of the sudoku board and backtrack if it ever
        reaches a non-valid state.
        :param row: int
        :param col: int
        :return: bool
        """
        current_row = row
        current_col = col

        # If program makes it to the right edge of the board,
        # move to the first element of the next row
        if current_col == len(self.board[current_row]):
            current_row += 1
            current_col = 0

            # If program makes it to the right edge of the last row,
            # it has reached a solution. Return True.
            if current_row == len(self.board):
                return True
            
        # If value at current position is 0 (meaning it needs a value),
        # call try_digits_at_position which will try all possible digits (1-9)
        # at the current position and continue to try to solve board in new state.
        if self.board[current_row][current_col] == 0:
            return self.try_digits_at_position(current_row, current_col)
        
        # If value != 0, move on to the next tile.
        return self.solve_partial_sudoku(current_row, current_col + 1)
    
    def try_digits_at_position(self, row, col):
        """
        Try all possible digits (1-9) in current position and 
        continue to try to solve the board in its new state.
        """
        for digit in range(1, 10): # board will always be a 9x9

            self.redraw(digit, row, col)

            # Pauses the algorithm at each iteration so a human can see what it's doing.
            pygame.time.delay(50) # 50 ms delay

            if self.is_valid_at_position(digit, row, col):
                # If digit is valid in current board state, insert it.
                self.board[row][col] = digit
                # Need to change tile's value attribute too so it prints to screen.
                self.tiles[row][col].set_val(digit)
 
                # Try to solve rest of board with new value inserted
                if self.solve_partial_sudoku(row, col):
                    return True
            
            # If unable to solve the board with any value in current position,
            # reset value in current position to 0 and return False.
            self.board[row][col] = 0
            self.tiles[row][col].set_val(0)
            self.tiles[row][col].backtrack = True
            
        # Returning False will cause solve_partial_sudoku to backtrack
        return False
    
    def is_valid_at_position(self, value, row, col):
        """
        Determines whether a value at location (row, col) on board
        is valid in current board state.
        """
        row_is_valid = value not in self.board[row]
        col_is_valid = value not in map(lambda r: r[col], self.board)

        if not row_is_valid or not col_is_valid:
            return False

        # Check values in sub-grid
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3

        # Calculate and search through indeces of all rows and cols in subgrid
        for row_idx in range(3):
            for col_idx in range(3):
                row_to_check = subgrid_row_start + row_idx
                col_to_check = subgrid_col_start + col_idx

                existing_value = self.board[row_to_check][col_to_check]

                # If any value in the subgrid is equal to the value we 
                # are trying to place, return False.
                if existing_value == value:
                    return False
        
        # Value is valid
        self.tiles[row][col].backtrack = False
        self.tiles[row][col].draw_border()
        return True

    def redraw(self, digit, row, col):
        """
        Redraws the board at every attempt of try_digits_at_position
        to show the algorithm's process.
        """
        
        self.deselect_all_tiles()

        # Set tiles temp value to current attempt
        self.tiles[row][col].set_temp_val(digit)
        
        # redraw tile and background with current temp value and border color
        self.tiles[row][col].draw_tile(BLACK)
        self.tiles[row][col].draw_border()

        pygame.display.update()

    def check_answer(self):
        """
        Check user's answer after they have pressed Enter to submit a value.
        """
        row = self.selected_tile.row
        col = self.selected_tile.col

        # If user submits an incorrect answer
        if self.selected_tile.temp != self.solved_board[row][col]:
            # make text red and pause
            self.selected_tile.draw_tile(RED)
            pygame.display.update()
            pygame.time.delay(1000) # 1000 ms (1 sec) delay

            # reset temp value 0
            self.selected_tile.temp = 0

        else: # If user submits a correct answer
            # make text green and pause
            self.selected_tile.draw_tile(GREEN)
            pygame.display.update()
            pygame.time.delay(1000) # 1000 ms (1 sec) delay

            # set value to inserted temp value
            self.selected_tile.value = self.selected_tile.temp
            # reset temp value to 0
            self.selected_tile.temp = 0
            # Make tile immutable
            self.selected_tile.is_immutable = True
        
        # Deselect any tiles
        self.selected_tile = None
        self.deselect_all_tiles()
