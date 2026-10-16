

import pygame
import random

pygame.init()


class Configuration:
    block_size = 30

    grid_col_num = 10
    grid_row_num = 20

    grid_width  = grid_col_num * block_size
    grid_height = grid_row_num * block_size

    frame_width  = grid_width + 200
    frame_height = grid_height

    frame_rate = 60

    fall_time  = 0
    fall_speed = 400

    big_font   = pygame.font.SysFont("arial", 36)
    small_font = pygame.font.SysFont("arial", 30)


CFG = Configuration()


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY  = (100, 100, 100)

    RED   = (255, 0, 0)
    BLUE  = (0, 0, 255)
    GREEN = (0, 255, 0)

    YELLOW = (255, 255, 0)
    ORANGE = (255, 150, 0)
    PINK   = (255, 0, 255)
    PURPLE = (150, 0, 255)

COL = Colors()


BLOCK_SHAPES = [
    [[1, 1, 1, 1]], # I shape
    [
        [1, 0, 0],  # J shape
        [1, 1, 1]
    ],
    [
        [0, 0, 1],  # L shape
        [1, 1, 1]
    ],
    [
        [1, 1],     # O shape
        [1, 1]
    ],
    [
        [0, 1, 1],  # S shape
        [1, 1, 0]
    ],
    [
        [0, 1, 0],  # T shape
        [1, 1, 1]
    ],
    [
        [1, 1, 0],  # Z shape
        [0, 1, 1]
    ]
]


BLOCK_COLORS = [
    COL.BLACK,
    COL.RED,
    COL.GREEN,
    COL.BLUE,
    COL.YELLOW,
    COL.ORANGE,
    COL.PINK,
    COL.PURPLE
]


class Tetris:
    def __init__(self):
        self.grid = [
            [0 for _ in range(CFG.grid_col_num)]
            for _ in range(CFG.grid_row_num)
        ]

        self.current_block = self.new_piece()
        self.current_X = CFG.grid_col_num // 2
        - len(self.current_block[0]) // 2

        self.current_Y = -1

        self.current_color = random.randint(1, len(BLOCK_COLORS) - 1)

        self.game_over = False
        self.score = 0

    def new_piece(self):
        return random.choice(BLOCK_SHAPES)

    def check_collision(self, block_shape, offset_x, offset_y):
        for r_idx, row in enumerate(block_shape):
            for c_idx, val in enumerate(row):
                if val != 0:
                    board_x = offset_x + c_idx
                    board_y = offset_y + r_idx

                    # CHECK COLLISION WITH BLOCKS
                    if (
                        board_x < 0 or
                        board_x >= CFG.grid_col_num or
                        board_y >= CFG.grid_row_num
                    ):
                        return True

                    if board_y >= 0 and self.grid[board_y][board_x] != 0:
                        return True
        return False

    def merge_piece(self):
        for r_idx, row in enumerate(self.current_block):
            for c_idx, val in enumerate(row):
                if val != 0:
                    board_x = self.current_X + c_idx
                    board_y = self.current_Y + r_idx

                    if (
                        0 <= board_y < CFG.grid_row_num
                        and 0 <= board_x < CFG.grid_col_num
                    ):
                        # FILL BLOCK VALUES WITH COLOR INDEX
                        self.grid[board_y][board_x] = self.current_color

    def clear_lines(self):
        full_rows = [
            i for i, row in enumerate(self.grid)
            if all(cell != 0 for cell in row)
        ]

        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [0 for _ in range(CFG.grid_col_num)])

        if full_rows:
            self.score += len(full_rows) * 100

    def rotate_piece(self):
        """
        current_shape = [
            [1, 0, 0],
            [1, 1, 1]
        ]

        Search backward algorithm: list[start:stop:step]
        if start is blank: start from 0
        if stop is blank: stop at the end

        current_shape[::-1]
        ->  [
                [2, 2, 2],
                [2, 0, 0]
            ]

        Break down:
        *current_shape[::-1]
        -> 1. [2, 2, 2]
        -> 2. [2, 0, 0]

        Merge:
        zip(*current_shape[::-1])
        ->  1. (2, 2)
        ->  2. (2, 0)
        ->  3. (2, 0)

        Convert to list:
        [
            list(row)
            for row in zip(*current_shape[::-1])
        ]

        ->  [
                [2, 2],
                [2, 0],
                [2, 0]
            ]
        """

        rotated = [
            list(row)
            for row in zip(*self.current_block[::-1])
        ]

        if not self.check_collision(
            rotated,
            self.current_X,
            self.current_Y
        ):
            self.current_block = rotated

    def drop(self):
        if not self.check_collision(
            self.current_block,
            self.current_X,
            self.current_Y + 1
        ):
            self.current_Y += 1

        else:
            self.merge_piece()
            self.clear_lines()

            self.current_block = self.new_piece()
            self.current_X = CFG.grid_col_num // 2
            - len(self.current_block[0]) // 2

            self.current_Y = 0

            self.current_color = random.randint(1, len(BLOCK_COLORS) - 1)

            if self.check_collision(
                self.current_block,
                self.current_X,
                self.current_Y
            ):
                self.game_over = True

    def move(self, dx):
        new_x = self.current_X + dx
        if not self.check_collision(
            self.current_block,
            new_x,
            self.current_Y
        ):
            self.current_X = new_x


def draw_grid(window):
    for i in range(CFG.grid_col_num + 1):
        pygame.draw.line(
            window,
            COL.GRAY,
            (i * CFG.block_size, 0),
            (i * CFG.block_size, CFG.grid_height), 1
        )

    for j in range(CFG.grid_row_num + 1):
        pygame.draw.line(
            window,
            COL.GRAY,
            (0, j * CFG.block_size),
            (CFG.grid_width, j * CFG.block_size), 1
        )


def main():
    window = pygame.display.set_mode((CFG.frame_width, CFG.frame_height))
    clock = pygame.time.Clock()

    game = Tetris()

    title = CFG.big_font.render("TETRIS", True, COL.WHITE)

    running = True
    while running:
        dt = clock.tick(CFG.frame_rate)
        CFG.fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_DOWN:
                    game.drop()

        # FALLING BLOCK
        if not game.game_over and CFG.fall_time >= CFG.fall_speed:
            game.drop()
            CFG.fall_time = 0

        window.fill(COL.BLACK)
        window.blit(title, (CFG.grid_width + 20, 20))

        score = CFG.small_font.render(f"Score: {game.score}", True, COL.WHITE)
        window.blit(score, (CFG.grid_width + 20, 70))

        draw_grid(window)

        """
        ------------------------------------------
        DRAW POSITION-FIXED BLOCKS
        ------------------------------------------
        Search all none-zero cell in the grid,
        cell value = color index
        """
        for r in range(CFG.grid_row_num):
            for c in range(CFG.grid_col_num):
                if game.grid[r][c] != 0:
                    pygame.draw.rect(window, BLOCK_COLORS[game.grid[r][c]], (c * CFG.block_size, r * CFG.block_size, CFG.block_size - 1, CFG.block_size - 1))

        # DRAW DROPPING BLOCK
        if not game.game_over:
            for r_idx, row in enumerate(game.current_block):
                for c_idx, val in enumerate(row):
                    if val != 0:
                        x = (game.current_X + c_idx) * CFG.block_size
                        y = (game.current_Y + r_idx) * CFG.block_size

                        pygame.draw.rect(
                            window,
                            BLOCK_COLORS[game.current_color],
                            (x, y, CFG.block_size - 1, CFG.block_size - 1)
                        )
        
        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()