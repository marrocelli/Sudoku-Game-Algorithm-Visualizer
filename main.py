import pygame
import time
from board import Board

# initialize pygame font library
pygame.font.init()

# GLOBAL CONSTANTS
WIDTH, HEIGHT = 400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Create main surface/window
pygame.display.set_caption("Sudoku")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def draw_window(board):
    """
    Handles drawing objects to screen.
    :param board: Board
    :return: None
    """
    WIN.fill(WHITE)
    board.draw_board()
    pygame.display.update()

def main():
    """
    Manages gameplay.
    """
    board = Board(WIDTH, HEIGHT, WIN)
    key_value = 0
    

    run = True
    while run:

        for event in pygame.event.get():

            # If player closes the window, quit game.
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Handle clicks
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                board.select_clicked_tile(mouse_pos)

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                # Handle number key presses (fill tile with key_value)
                if event.key == pygame.K_1:
                    key_value = 1
                if event.key == pygame.K_2:
                    key_value = 2
                if event.key == pygame.K_3:
                    key_value = 3
                if event.key == pygame.K_4:
                    key_value = 4
                if event.key == pygame.K_5:
                    key_value = 5
                if event.key == pygame.K_6:
                    key_value = 6
                if event.key == pygame.K_7:
                    key_value = 7
                if event.key == pygame.K_8:
                    key_value = 8
                if event.key == pygame.K_9:
                    key_value = 9
                if event.key == pygame.K_BACKSPACE:
                    # Setting key value to 0 will remove the temp value
                    key_value = 0
                if event.key == pygame.K_RETURN:
                    # Submit number and check answer
                    if board.selected_tile:
                        board.check_answer()
                    
                # Handle Space Key press (solve board)
                if event.key == pygame.K_SPACE:
                    board.solve()
        
        # Set the temp value to the pressed key value if a tile
        # is selected and a key has been pressed.
        if board.selected_tile:
            board.selected_tile.set_temp_val(key_value if key_value else 0)


        draw_window(board)


if __name__ == "__main__":
    main()
