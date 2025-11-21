import pygame
import random
import sys

# ----------------------------
# Auto Screen Configuration
# ----------------------------
pygame.init()
info = pygame.display.Info()
SCREEN_W, SCREEN_H = info.current_w, info.current_h

# Set window as a square based on the shortest side
WINDOW_SIZE = min(SCREEN_W, SCREEN_H) - 100  # margin for safety
BOARD_SIZE = 4  # 4x4 puzzle (15 puzzle)
TILE_SIZE = WINDOW_SIZE // BOARD_SIZE
FPS = 60

win = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 60))
pygame.display.set_caption("Slide Puzzle Game - Auto Screen Edition")
font = pygame.font.SysFont("Arial", WINDOW_SIZE // 12, bold=True)
small_font = pygame.font.SysFont("Arial", WINDOW_SIZE // 20)

# ----------------------------
# Create Board
# ----------------------------
def create_board():
    nums = list(range(1, BOARD_SIZE * BOARD_SIZE))
    nums.append(0)
    random.shuffle(nums)

    while not is_solvable(nums):
        random.shuffle(nums)

    board = []
    for i in range(0, len(nums), BOARD_SIZE):
        board.append(nums[i:i + BOARD_SIZE])
    return board


def is_solvable(nums):
    inv_count = 0
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if nums[i] and nums[j] and nums[i] > nums[j]:
                inv_count += 1
    return inv_count % 2 == 0

# ----------------------------
# Draw Board
# ----------------------------
def draw_board(board, moves):
    win.fill((30, 30, 30))

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            value = board[r][c]

            if value != 0:
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                pygame.draw.rect(win, (70, 130, 180),
                                 (x + 3, y + 3, TILE_SIZE - 6, TILE_SIZE - 6), border_radius=10)

                text = font.render(str(value), True, (255, 255, 255))
                win.blit(text, (x + TILE_SIZE // 2 - text.get_width() // 2,
                                y + TILE_SIZE // 2 - text.get_height() // 2))

    # Info panel
    pygame.draw.rect(win, (20, 20, 20), (0, WINDOW_SIZE, WINDOW_SIZE, 60))
    moves_text = small_font.render(f"Langkah: {moves}", True, (255, 255, 255))
    win.blit(moves_text, (20, WINDOW_SIZE + 15))

    pygame.display.update()

# ----------------------------
# Tile Logic
# ----------------------------
def get_empty(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == 0:
                return r, c
    return None


def move_tile(board, r, c):
    er, ec = get_empty(board)
    if abs(er - r) + abs(ec - c) == 1:
        board[er][ec], board[r][c] = board[r][c], board[er][ec]
        return True
    return False


def is_solved(board):
    correct = list(range(1, BOARD_SIZE * BOARD_SIZE)) + [0]
    flat = [num for row in board for num in row]
    return flat == correct

# ----------------------------
# Main Game Loop
# ----------------------------
def main():
    board = create_board()
    clock = pygame.time.Clock()
    moves = 0

    while True:
        clock.tick(FPS)
        draw_board(board, moves)

        if is_solved(board):
            win.fill((20, 20, 20))
            msg = font.render("Puzzle Selesai!", True, (0, 255, 100))
            win.blit(msg, (WINDOW_SIZE // 2 - msg.get_width() // 2,
                           WINDOW_SIZE // 2 - msg.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            return main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < WINDOW_SIZE:
                    c = x // TILE_SIZE
                    r = y // TILE_SIZE
                    if move_tile(board, r, c):
                        moves += 1

main()
