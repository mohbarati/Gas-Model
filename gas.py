import pygame
from pygame.locals import *
from math import sqrt
from time import sleep

pygame.init()
sc = pygame.display.set_mode((600, 600))
red = (255, 0, 0)
blue = (100, 100, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (30, 60, 30)
sc.fill(black)


class ball:
    k = 1

    def __init__(self, x, y, r, color, vx, vy, m):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.m = m

    def __distance(self, x, y):
        return sqrt(x**2 + y**2)

    def draw_ball(self):
        pygame.draw.circle(sc, self.color, (self.x, self.y), self.r)

    def erase_ball(self):
        pygame.draw.circle(sc, black, (self.x, self.y), self.r)

    def collision_detection(self, new):
        if (
            self.__distance(
                (self.x) - (new.x),
                (self.y) - (new.y),
            )
            <= self.r + new.r
        ):
            return True
        return False

    def force_balls(self, new):
        del_x = self.x - new.x
        del_y = self.y - new.y
        distance = self.__distance(del_x, del_y)
        f = -self.k * (distance - (self.r + new.r))
        return f * del_x / distance, f * del_y / distance

    def __wall_force(self, w, b):
        pass

    def wall_collide(self, wall):
        k_wall = 1000
        f = self.__wall_force(self.x, 0)


# -----------------
ball1 = ball(100, 100, 20, red, 2, 3, 1)
ball2 = ball(100, 121, 20, blue, -1, -3, 1)
ball1.draw_ball()
ball2.draw_ball()
pygame.display.update()
cont = True
dt = 0.001
while cont:

    if ball1.collision_detection(ball2):
        ball1.draw_ball()
        ball2.draw_ball()
        pygame.display.update()
        f1x, f1y = ball1.force_balls(ball2)
        f2x, f2y = -f1x, -f1y
        a1x = f1x / ball1.m
        a2x = f2x / ball2.m
        a1y = f1y / ball1.m
        a2y = f2y / ball2.m
        ball1.vx += a1x * dt
        ball1.vy += a1y * dt
        ball2.vx += a2x * dt
        ball2.vy += a2y * dt
        ball1.x += dt * ball1.vx
        ball2.x += dt * ball2.vx
        ball1.y += dt * ball1.vy
        ball2.y += dt * ball2.vy
        sc.fill(black)
    ball1.x += dt * ball1.vx
    ball2.x += dt * ball2.vx
    ball1.y += dt * ball1.vy
    ball2.y += dt * ball2.vy
    ball1.draw_ball()
    ball2.draw_ball()
    pygame.display.update()

    # if x > 600:
    #     vx = -vx
    # if y > 600:
    #     vy = -vy
    # if x < 0:
    #     vx = -vx
    # if y < 0:
    #     vy = -vy
    # draw_circle(yellow, x, y, r)
    # pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == K_q:
                cont = False
        if event.type == QUIT:
            cont = False
    sc.fill(black)
pygame.quit()
