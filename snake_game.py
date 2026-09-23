
import pygame
from random import randint
from collections import deque


pygame.init()

CFG = {
    "BLACK": (  0,   0,   0),
    "WHITE": (255, 255, 255),
    "GREEN": (  0, 255,   0),
    "RED"  : (255,   0,   0),

    "grid_size" : (20, 20),
    "frame_size": (600, 600),

    "big_font"  : pygame.font.SysFont("Arial", 48),
    "small_font": pygame.font.SysFont("Arial", 24)
}

screen = pygame.display.set_mode(CFG["frame_size"])
clock  = pygame.time.Clock()


class Snake:
    def __init__(self, coord: list, dir: str):
        self.coord = coord
        self.body = [coord]
        self.body_hist = deque(maxlen=2)

        self.running = True

        self.dir = dir
        self.last_dir = self.dir

        self.grow = False
    
    def draw_snake(self):
        step = CFG["frame_size"][0]//CFG["grid_size"][0]

        if len(self.body_hist) == 2:
            for part in self.body_hist[0]:
                start = [part[0]*step, part[1]*step]

                pygame.draw.rect(
                    screen,
                    CFG["GREEN"],
                    (start[0], start[1], step, step)
                )
    
    def get_run(self, head):
        board = CFG["grid_size"]

        for i, coord in enumerate(head):
            if coord > board[i]-1 or coord < 0:
                self.running = False
        
        if len(self.body) > 2:
            for part in self.body[:-2]:
                if part == head:
                    self.running = False
    
    def get_grow(self, head, apple_pos: list):
        if head == apple_pos:
            self.grow = True
        else:
            self.grow = False
    
    def run(self, apple_pos: list):
        head = self.body[-1].copy()

        self.dir = self.last_dir

        if self.dir == "RIGHT":
            head[0] += 1
        elif self.dir == "LEFT":
            head[0] -= 1
        elif self.dir == "UP":
            head[1] -= 1
        elif self.dir == "DOWN":
            head[1] += 1
            
        self.get_run(head)
        self.get_grow(head, apple_pos)
        if self.running:
            self.body.append(head)
            if not self.grow:
                self.body.pop(0)
            
        self.body_hist.append(self.body)
        self.draw_snake()


class Apple:
    def __init__(self):
        self.pos = self.get_rand_pos()
    
    def get_rand_pos(self):
        new_pos = [randint(0, CFG["grid_size"][0]-1), randint(0, CFG["grid_size"][1]-1)]
        return new_pos
    
    def draw_apple(self):
        step = CFG["frame_size"][0]//CFG["grid_size"][0]
        pos  = [self.pos[0]*step, self.pos[1]*step]

        pygame.draw.rect(
            screen,
            CFG["RED"],
            (pos[0], pos[1], step, step)
        )


def game_over(snake_run: bool, score: int):
    game_run = True
    if not snake_run:
        game_run = False

    if not game_run:
        font1 = CFG["big_font"]
        text1 = font1.render(
            "GAME OVER",
            True,
            CFG["WHITE"]
        )
        text_rect1 = text1.get_rect(
            center=(
                CFG["frame_size"][0] // 2,
                CFG["frame_size"][1] // 2
            )
        )
        screen.blit(text1, text_rect1)


        font2 = CFG["big_font"]
        text2 = font2.render(
            f"Your score: {score}",
            True,
            CFG["WHITE"]
        )
        text_rect2 = text2.get_rect(
            center=(
                CFG["frame_size"][0] // 2,
                CFG["frame_size"][1] // 2 + 50
            )
        )
        screen.blit(text2, text_rect2)


        font3 = CFG["small_font"]
        text3 = font3.render(
            "Press SPACE to play again",
            True,
            CFG["WHITE"]
        )
        text_rect3 = text3.get_rect(
            center=(
                CFG["frame_size"][0] // 2,
                CFG["frame_size"][1] // 2 + 100
            )
        )
        screen.blit(text3, text_rect3)


def scoring(score: int):
    font = CFG["small_font"]
    text = font.render(
        f"score: {score}",
        True,
        CFG["WHITE"]
    )
    screen.blit(text, (10, 10))


def draw_grid():
    step = CFG["frame_size"][0]//CFG["grid_size"][0]
    thickness = 1

    for i in range(0, CFG["frame_size"][0]+1, step):
        pygame.draw.line(
            screen,
            CFG["WHITE"],
            (i, 0),
            (i, CFG["frame_size"][1]),
            thickness
        )

    for j in range(0, CFG["frame_size"][1]+1, step):
        pygame.draw.line(
            screen,
            CFG["WHITE"],
            (0, j),
            (CFG["frame_size"][0], j),
            thickness
        )


def draw_board():
    screen.fill(CFG["BLACK"])
    draw_grid()


def main():
    snake = Snake([0, 0], "RIGHT")
    apple = Apple()
    score = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.dir != "DOWN":
                    snake.last_dir = "UP"
                if event.key == pygame.K_DOWN and snake.dir != "UP":
                    snake.last_dir = "DOWN"
                if event.key == pygame.K_LEFT and snake.dir != "RIGHT":
                    snake.last_dir = "LEFT"
                if event.key == pygame.K_RIGHT and snake.dir != "LEFT":
                    snake.last_dir = "RIGHT"
                if event.key == pygame.K_SPACE and snake.running == False:
                    snake = Snake([0, 0], "RIGHT")
                    apple = Apple()
                    score = 0

        
        draw_board()
        apple.draw_apple()
        snake.run(apple.pos)

        if snake.grow:
            apple.pos = apple.get_rand_pos()
            score += 1
        
        scoring(score)
        game_over(snake.running, score)

        pygame.display.flip()
        clock.tick(8)

    pygame.quit()

if __name__=="__main__":
    main()