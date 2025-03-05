import pygame
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 2
FONT_SIZE = 40

# Function to check if a number can be placed in a specific row, column, and 3x3 subgrid
def is_valid(board, row, col, num):
    # Check the row
    for i in range(9):
        if board[row][i] == num:
            return False
    
    # Check the column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

# Backtracking function to solve the Sudoku puzzle step-by-step
class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.steps = []  # Will store the evolution of the board
        self.solving = False  # Flag to control the solver's state
        self.solve_sudoku()  # Start solving the puzzle
    
    def solve_sudoku(self):
        self.steps = []  # Reset steps when starting a new solution
        self._solve_recursive(self.board)
    
    def _solve_recursive(self, board):
        # Find the first empty cell (denoted by 0)
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    # Try every number from 1 to 9
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            self.steps.append([row, col, num, [row[:] for row in board], True])  # Save state with correct placement
                            if self._solve_recursive(board):
                                return True
                            board[row][col] = 0  # Backtrack
                    return False
        return True
    
    def get_next_step(self):
        if self.steps:
            step = self.steps.pop(0)
            return step[3], step[0], step[1], step[2]  # return the updated board and position/number
        return None

# Function to draw the board on pygame window
def draw_board(board, screen, initial_board, steps, step_index):
    screen.fill((255, 255, 255))  # Fill screen with white background


    # Draw numbers with colors
    font = pygame.font.Font(None, FONT_SIZE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = board[row][col]
            is_fixed = initial_board[row][col] != 0  # Check if the cell is fixed
            is_correct = value != 0 and is_valid(board, row, col, value)  # Check if the cell value is correct

            if is_fixed:
                # Color fixed cells grey
                cell_color = (200, 200, 200)  # Grey for fixed cells
            elif is_correct:
                # Color correctly filled cells green
                cell_color = (0, 255, 0)  # Green for correct cells
            else:
                # Color incorrect cells red
                cell_color = (255, 255, 255)  # Red for incorrect cells

            # Fill the cell background with color
            pygame.draw.rect(screen, cell_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw the number
            if value != 0:
                number_text = font.render(str(value), True, (0, 0, 0))
                screen.blit(number_text, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 3))
    # Draw grid lines
    for row in range(GRID_SIZE + 1):
        line_width = LINE_WIDTH if row % 3 != 0 else 4  # Thicker lines for subgrid boundaries
        pygame.draw.line(screen, (0, 0, 0), (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), line_width)  # Horizontal
        pygame.draw.line(screen, (0, 0, 0), (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), line_width)  # Vertical

    pygame.display.update()

# Initial Sudoku board
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Make a copy of the initial board to track fixed cells
initial_board = [row[:] for row in sudoku_board]

# Setup pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver Step-by-Step")

# Initialize Sudoku solver
solver = SudokuSolver(sudoku_board)

# Display the initial board
draw_board(solver.board, screen, initial_board, solver.steps, 0)
time.sleep(1)  # Wait a bit before starting the steps

# Main game loop
running = True
step_index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # If there are steps left, update the board and display it
    if step_index < len(solver.steps):
        updated_board = solver.steps[step_index][3]  # Get the updated board for the current step
        draw_board(updated_board, screen, initial_board, solver.steps, step_index)  # Redraw the board
        step_index += 1
        time.sleep(0.001)  # Add a delay between steps

    # Keep updating the screen
    pygame.display.update()

pygame.quit()
