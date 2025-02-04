import os
import pygame
import time
import copy

# Inicialización de Pygame
pygame.init()

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Configuración de la pantalla
margin = 50
tile_size = 60
width = height = tile_size * 9 + 2 * margin
button_height = 50
screen = pygame.display.set_mode((width, height + button_height))
pygame.display.set_caption("Sudoku Solver")

# Fuente
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)
solved = False

def draw_grid(board, fixed_numbers):
    screen.fill(WHITE)
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (margin, margin + i * tile_size), (width - margin, margin + i * tile_size), thickness)
        pygame.draw.line(screen, BLACK, (margin + i * tile_size, margin), (margin + i * tile_size, height - margin), thickness)
    
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                color = BLACK if fixed_numbers[row][col] else BLUE
                text = font.render(str(board[row][col]), True, color)
                screen.blit(text, (margin + col * tile_size + 20, margin + row * tile_size + 15))
    
    pygame.draw.rect(screen, GRAY, (margin, height, width - 2 * margin, button_height))
    button_text = button_font.render("Solve Sudoku", True, BLACK)
    screen.blit(button_text, (width // 2 - 60, height + 15))
    
    if solved:
        solved_text = button_font.render("RESUELTO", True, RED)
        screen.blit(solved_text, (width // 2 - 40, height // 2 - 10))
    
    pygame.display.flip()

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j  # Fila, Columna
    return None

def is_valid(board, num, pos):
    row, col = pos
    for i in range(9):
        if board[row][i] == num and col != i:
            return False
    for i in range(9):
        if board[i][col] == num and row != i:
            return False
    box_x, box_y = col // 3, row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def solve_sudoku(board, fixed_numbers):
    global solved
    empty = find_empty(board)
    if not empty:
        solved = True
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            draw_grid(board, fixed_numbers)
            time.sleep(0.1)
            if solve_sudoku(board, fixed_numbers):
                return True
            board[row][col] = 0
            draw_grid(board, fixed_numbers)
            time.sleep(0.1)
    return False

def get_board_input():
    board = [[0] * 9 for _ in range(9)]
    fixed_numbers = [[False] * 9 for _ in range(9)]
    running = True
    selected = None
    solving = False
    while running:
        screen.fill(WHITE)
        draw_grid(board, fixed_numbers)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if margin <= x <= width - margin and margin <= y <= height - margin:
                    selected = ((y - margin) // tile_size, (x - margin) // tile_size)
                elif height <= y <= height + button_height:
                    solving = True
            elif event.type == pygame.KEYDOWN and selected and not fixed_numbers[selected[0]][selected[1]]:
                if event.unicode.isdigit():
                    num = int(event.unicode)
                    if 1 <= num <= 9:
                        board[selected[0]][selected[1]] = num
                        fixed_numbers[selected[0]][selected[1]] = True
        pygame.display.flip()
        if solving:
            solve_sudoku(board, fixed_numbers)
            solving = False
    return board

def main():
    board = get_board_input()
    pygame.quit()

if __name__ == "__main__":
    main()
