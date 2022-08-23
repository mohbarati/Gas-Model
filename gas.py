from math import sqrt

import pygame
from pygame.locals import *

pygame.init()
sc = pygame.display.set_mode((600, 600))
red = (255, 0, 0)
blue = (100, 100, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (30, 60, 30)
sc.fill(black)


class ball:
    """Making instances of a ball and its atributes
    """

    k = 1000

    def __init__(self, x, y, r, color, vx, vy, m):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.m = m

    def __distance(self, x, y):
        return sqrt(x ** 2 + y ** 2)

    def draw_ball(self):
        pygame.draw.circle(sc, self.color, (self.x, self.y), self.r)

    def erase_ball(self):
        pygame.draw.circle(sc, black, (self.x, self.y), self.r)

    def collision_detection(self, new):
        if self.__distance((self.x) - (new.x), (self.y) - (new.y),) <= self.r + new.r:
            return True
        return False

    def force_balls(self, new):
        del_x = self.x - new.x
        del_y = self.y - new.y
        distance = self.__distance(del_x, del_y)
        f = -new.k * (distance - (self.r + new.r))
        return f * del_x / distance, f * del_y / distance

    def __wall_force(self, wall, obj):
        return -self.k * abs(wall - obj)

    def wall_collide(self, wall):
        k_wall = 1000
        f = self.__wall_force(self.x, 0)
        return f / self.m


class wall(ball):
    r = 0
    k = 1000

    def __init__(self, x, y):
        self.x = x
        self.y = y


# -----------------
ball1 = ball(50, 50, 20, red, 10, 2, 1)
ball2 = ball(70, 70, 25, blue, 30, 4, 1)
ball3 = ball(90, 90, 30, blue, 50, 6, 1)
ball4 = ball(120, 121, 10, blue, 7, 80, 1)
ball5 = ball(160, 160, 15, blue, 9, 10, 1)
objects = [ball1, ball2, ball3, ball4, ball5]

wall_top = wall(None, 0)
wall_down = wall(None, 600)
wall_left = wall(0, None)
wall_right = wall(600, None)

for obj in objects:
    obj.draw_ball()
pygame.display.update()

cont = True
dt = 0.01
while cont:
    for i, obj in enumerate(objects):
        for new_obj in objects[i + 1 :]:
            if obj.collision_detection(new_obj):
                f1x, f1y = obj.force_balls(new_obj)
                f2x, f2y = -f1x, -f1y
                a1x = f1x / obj.m
                a1y = f1y / obj.m
                a2x = f2x / new_obj.m
                a2y = f2y / new_obj.m
                obj.vx += a1x * dt
                obj.vy += a1y * dt
                obj.x += dt * obj.vx
                obj.y += dt * obj.vy
                new_obj.vx += a2x * dt
                new_obj.vy += a2y * dt
                new_obj.x += dt * new_obj.vx
                new_obj.y += dt * new_obj.vy
            else:
                obj.x += dt * obj.vx
                obj.y += dt * obj.vy
        if obj.y <= obj.r:
            wall_top.x = obj.x
            Fx, Fy = obj.force_balls(wall_top)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
            obj.x += dt * obj.vx
            obj.y += dt * obj.vy
        elif obj.y >= 600 - obj.r:
            wall_down.x = obj.x
            Fx, Fy = obj.force_balls(wall_down)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
            obj.x += dt * obj.vx
            obj.y += dt * obj.vy
        if obj.x <= obj.r:
            wall_left.y = obj.y
            Fx, Fy = obj.force_balls(wall_left)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
            obj.x += dt * obj.vx
            obj.y += dt * obj.vy
        elif obj.x >= 600 - obj.r:
            wall_right.y = obj.y
            Fx, Fy = obj.force_balls(wall_right)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
            obj.x += dt * obj.vx
            obj.y += dt * obj.vy

    sc.fill(black)
    for obj in objects:
        obj.draw_ball()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == K_q:
                cont = False
        if event.type == QUIT:
            cont = False
pygame.quit()
