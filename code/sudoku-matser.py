try:
    import pygame
    import time
    import copy
except ImportError:
    import os
    os.system('pip install pygame')
    import pygame
    import time
    import copy

# Inicialización de Pygame
pygame.init()

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
GRAY = (200, 200, 200)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
HIGHLIGHT = (200, 220, 255, 100)
YELLOW = (255, 255, 0)

# Configuración de la pantalla
margin = 50
tile_size = 60
width = height = tile_size * 9 + 2 * margin
button_height = 60
screen = pygame.display.set_mode((width, height + button_height))
pygame.display.set_caption("Sudoku Solver")

# Fuente
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 70)
credit_font = pygame.font.Font(None, 30)
solved = False

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x, box_y = (col // 3) * 3, (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_y + i][box_x + j] == num:
                return False
    return True

def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def solve_sudoku(board, fixed_numbers):
    global solved
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        solved = True
        return True
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board, fixed_numbers):
                return True
            board[row][col] = 0
    return False

def draw_initial_screen():
    screen.fill(LIGHT_GRAY)
    title_text = title_font.render("Sudoku Master", True, BLACK)
    screen.blit(title_text, (width // 2 - 150, height // 3))
    
    button_rect = pygame.Rect(width // 2 - 100, height // 2, 200, 60)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)
    button_text = button_font.render("Iniciar Sudoku", True, WHITE)
    screen.blit(button_text, (width // 2 - 90, height // 2 + 10))
    
    credit_text = credit_font.render("by DevSergiJaume", True, DARK_GRAY)
    screen.blit(credit_text, (width - 180, height - 40))
    pygame.display.flip()
    
    return button_rect

def draw_grid(board, fixed_numbers, selected_cell=None):
    screen.fill(LIGHT_GRAY)
    pygame.draw.rect(screen, WHITE, (margin - 5, margin - 5, width - 2 * margin + 10, height - 2 * margin + 10), border_radius=10)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered_cell = None
    if margin <= mouse_x < width - margin and margin <= mouse_y < height - margin:
        hovered_cell = ((mouse_y - margin) // tile_size, (mouse_x - margin) // tile_size)
    
    for row in range(9):
        for col in range(9):
            cell_rect = pygame.Rect(margin + col * tile_size, margin + row * tile_size, tile_size, tile_size)
            if (row, col) == selected_cell:
                pygame.draw.rect(screen, HIGHLIGHT, cell_rect)
            elif hovered_cell and (row, col) == hovered_cell:
                pygame.draw.rect(screen, HIGHLIGHT, cell_rect)
            
            if board[row][col] != 0:
                color = BLACK if fixed_numbers[row][col] else BLUE
                text = font.render(str(board[row][col]), True, color)
                screen.blit(text, (margin + col * tile_size + 22, margin + row * tile_size + 10))
    
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 2
        pygame.draw.line(screen, DARK_GRAY, (margin, margin + i * tile_size), (width - margin, margin + i * tile_size), thickness)
        pygame.draw.line(screen, DARK_GRAY, (margin + i * tile_size, margin), (margin + i * tile_size, height - margin), thickness)
    
    button_rect = pygame.Rect(margin, height, width - 2 * margin, button_height)
    button_color = BUTTON_HOVER if button_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)
    button_text = button_font.render("Solve Sudoku", True, WHITE)
    screen.blit(button_text, (width // 2 - 80, height + 15))
    
    if solved:
        pygame.draw.rect(screen, YELLOW, (width // 2 - 120, height // 2 - 40, 240, 80))
        solved_text = pygame.font.Font(None, 80).render("RESUELTO", True, RED)
        screen.blit(solved_text, (width // 2 - 100, height // 2 - 30))
    
    pygame.display.flip()

def get_board_input():
    board = [[0] * 9 for _ in range(9)]
    fixed_numbers = [[False] * 9 for _ in range(9)]
    running = True
    selected = None
    solving = False
    while running:
        draw_grid(board, fixed_numbers, selected)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if margin <= x <= width - margin and margin <= y <= height - margin:
                    selected = ((y - margin) // tile_size, (x - margin) // tile_size)
                elif height <= y <= height + button_height:
                    solving = True
            elif event.type == pygame.KEYDOWN and selected:
                if event.unicode.isdigit():
                    num = int(event.unicode)
                    if 1 <= num <= 9:
                        board[selected[0]][selected[1]] = num
        pygame.display.flip()
        if solving:
            solve_sudoku(board, fixed_numbers)
            solving = False
    return board

def main():
    button_rect = draw_initial_screen()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
    board = get_board_input()
    pygame.quit()

if __name__ == "__main__":
    main()
