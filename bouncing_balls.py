
import numpy as np
import pygame
import math
from random import choice
from random import uniform

pygame.init()

class Configurations:
    FRAME_WIDTH  = 600
    FRAME_HEIGHT = 600
    clock = pygame.time.Clock()

    # GAME FEATURES
    gravity = 0.2
    # CIRCLE
    circleCenter = (FRAME_WIDTH//2, FRAME_HEIGHT//2)
    circleRadius = int((max(FRAME_WIDTH, FRAME_HEIGHT) - 150) / 2)
    circleThick  = 2
    circleSpinSpeed = 0.02

    arcAngle = 60
    tri_Size = int((circleRadius**2 + (circleRadius*math.tan(arcAngle/2))**2)**(1/2)) + 10

    # BALL
    ballCenter = (
        circleCenter[0],
        circleCenter[1] - circleRadius + 100
    )
    ballRadius = 10
    

CFG = Configurations()

class Colors:
    BLACK  = (  0,   0,   0)
    BLUE   = (  0,   0, 255)
    CYAN   = (  0, 255, 255)
    WHITE  = (255, 255, 255)
    YELLOW = (255, 255,   0)
    RED    = (255,   0,   0)
    PURPLE = (255,   0, 255)

    Col_List = [
        BLUE,
        CYAN,
        PURPLE,
        RED,
        WHITE,
        YELLOW
    ]

COL = Colors()


class CreateCircle:
    def __init__(self, center, radius, thickness, color):
        self.CENTER = np.array(center, dtype=np.float64)
        self.RADIUS = radius
        self.THICK  = thickness
        self.COLOR  = color

    def draw(self, frame):
        pygame.draw.circle(
            frame,
            self.COLOR,
            self.CENTER,
            self.RADIUS,
            self.THICK
        )


class Circle(CreateCircle):
    def __init__(self, center, radius, thickness, color):
        super().__init__(center, radius, thickness, color)

        self.start_angle = math.radians(-CFG.arcAngle / 2)
        self.end_angle   = math.radians(CFG.arcAngle / 2)

    def draw_arc(self, frame):
        self.start_angle += CFG.circleSpinSpeed
        self.end_angle   += CFG.circleSpinSpeed

        self.pt1 = self.CENTER + CFG.tri_Size * np.array(
            (math.cos(self.start_angle), math.sin(self.start_angle)),
            dtype=np.float64
        )

        self.pt2 = self.CENTER + CFG.tri_Size * np.array(
            (math.cos(self.end_angle), math.sin(self.end_angle)),
            dtype=np.float64
        )

        pygame.draw.polygon(
            frame,
            COL.BLACK,
            [
                self.CENTER,
                self.pt1,
                self.pt2
            ]
        )


class Ball(CreateCircle):
    def __init__(self, center, radius, thickness=0, color=None):
        super().__init__(center, radius, thickness, color)

        self.vel = np.array(
            (uniform(-4, 4), uniform(-1, 1)), dtype=np.float64
        )
        self.COLOR = choice(COL.Col_List)
        self.is_in = True

    def in_arc(self, circle: Circle):
        dx, dy = self.CENTER - circle.CENTER
        angle  = math.atan2(dy, dx)

        circle.start_angle = circle.start_angle % (2*math.pi)
        circle.end_angle = circle.end_angle % (2*math.pi)

        if circle.start_angle > circle.end_angle:
            circle.end_angle += 2*math.pi

        if (circle.start_angle <= angle <= circle.end_angle
            or circle.start_angle <= angle + 2*math.pi <= circle.end_angle
        ): return True
        return False

    def get_velocity(self, circle: Circle):
        self.vel[1] += CFG.gravity
        self.CENTER += self.vel

        max_dist = circle.RADIUS - self.RADIUS
        dist = np.linalg.norm(self.CENTER - circle.CENTER)

        if dist >= max_dist:
            if self.in_arc(circle):
                self.is_in = False
                
            if self.is_in:
                n = self.CENTER - circle.CENTER
                t = np.array((-n[1], n[0]), dtype=np.float64) * CFG.circleSpinSpeed

                n_unit = n / np.linalg.norm(n)
                t_unit = t / np.linalg.norm(t)

                self.CENTER = circle.CENTER + n_unit * max_dist

                v_ver = np.dot(self.vel, n_unit) * n_unit
                v_hor = np.dot(self.vel, t_unit) * t_unit

                if np.dot(self.vel, n) > 0:
                    self.vel = v_hor - v_ver
                    spin_vel = t * CFG.circleSpinSpeed
                    self.vel += spin_vel

    def draw(self, frame, circle: Circle):
        self.get_velocity(circle)
        super().draw(frame)


def main():
    frame = pygame.display.set_mode(
        (CFG.FRAME_WIDTH, CFG.FRAME_HEIGHT)
    )

    circle = Circle(CFG.circleCenter,
                    CFG.circleRadius,
                    CFG.circleThick,
                    COL.WHITE)
    balls = [
        Ball(
            CFG.ballCenter,
            CFG.ballRadius
        )
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame.fill((0, 0, 0))
        circle.draw(frame)
        circle.draw_arc(frame)

        for ball in balls:
            if (
                ball.CENTER[0] < 0
                or ball.CENTER[0] > CFG.FRAME_WIDTH
                or ball.CENTER[1] < 0
                or ball.CENTER[1] > CFG.FRAME_HEIGHT
            ):
                balls.remove(ball)
                balls.append(
                    Ball(CFG.ballCenter,
                         CFG.ballRadius)
                )
                balls.append(
                    Ball(CFG.ballCenter,
                         CFG.ballRadius)
                )
            ball.draw(frame, circle)

        pygame.display.flip()
        CFG.clock.tick(60)

    pygame.quit()

if __name__=="__main__":
    main()