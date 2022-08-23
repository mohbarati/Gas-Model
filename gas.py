from math import sqrt
from random import uniform, choices
import pygame
from pygame.locals import *

# initializing the screen
pygame.init()
width, height = 600, 600
sc = pygame.display.set_mode((width, height))
color_range = range(50, 200)
white = (250, 230, 240)
sc.fill(white)


class ball:
    """Making instances of a ball and its atributes"""

    def __distance(self, x, y):
        """Finds the Euclidean distance"""
        return sqrt(x**2 + y**2)

    def draw_ball(self):
        pygame.draw.circle(sc, self.color, (self.x, self.y), self.r)

    def collision_detection(self, new):
        """returns true if the balls overlap"""
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
        """Force inserted on a ball caused by another ball of the wall
        modeled by a spring. Returns the force in both components"""
        del_x = self.x - new.x
        del_y = self.y - new.y
        distance = self.__distance(del_x, del_y)
        f = -new.k * (distance - (self.r + new.r))
        return f * del_x / distance, f * del_y / distance

    def update(self):
        """Upodate the position of the ball"""
        self.x += dt * self.vx
        self.y += dt * self.vy


class wall(ball):
    """Wall is modeled as a ball in the mirrored position and with high k value"""

    r = 0
    k = 10000

    def __init__(self, x, y):
        self.x = x
        self.y = y


# -----------------Solid
def solid(r=33, m=1, k=1000):
    """Aranged in such a way to almost fill the screen with some vibration"""
    pos = []
    for i in range(r, width, 2 * r):
        for j in range(r, height, 2 * r):
            pos.append((i, j))
    number_of_balls = len(pos)
    ball_list = [ball() for _ in range(number_of_balls)]
    for i, item in enumerate(ball_list):
        item.x, item.y = pos[i]
        item.k = k
        item.r = r
        item.m = m
        item.vx = uniform(-50, 50)
        item.vy = uniform(-50, 50)
        item.color = choices(color_range, k=3)
    return ball_list


# ------------------- liquid
def liquid(number_of_balls=200, r=25, m=1, k=10):
    """Balls take more area than the screen, hence overlap causes them to
    exibit liquid behaviour (sliding)"""
    ball_list = [ball() for _ in range(number_of_balls)]
    for item in ball_list:
        item.k = k
        item.r = r
        item.m = m
        item.x = uniform(0 + r, width - r)
        item.y = uniform(0 + r, height - r)
        item.vx = 0
        item.vy = 0
        item.color = choices(color_range, k=3)
    return ball_list


# ------------------------gas
def gas(r=20, m=1, k=100, number_of_balls=100):
    """gas modeled with elastic collisions. No atraction force between the atoms"""
    ball_list = [ball() for _ in range(number_of_balls)]
    for item in ball_list:
        item.k = k
        item.r = r
        item.m = m
        item.x = uniform(0 + r, width - r)
        item.y = uniform(0 + r, height - r)
        item.vx = uniform(-3, 3)
        item.vy = uniform(-3, 3)
        item.color = choices(color_range, k=3)
    return ball_list


# ------------------------------

# initializing the walls
wall_top = wall(None, 0)
wall_down = wall(None, height)
wall_left = wall(0, None)
wall_right = wall(width, None)

# defining the state
ball_list = gas()  # solid() or liquid() or gas()

# drawing the particles
for obj in ball_list:
    obj.draw_ball()
pygame.display.update()

# Starting the loop
dt = 0.01
cont = True

while cont:
    for i, obj in enumerate(ball_list):
        for new_obj in ball_list[i + 1 :]:  # collision of balls with each other
            if obj.collision_detection(new_obj):
                f1x, f1y = obj.force_balls(new_obj)
                f2x, f2y = -f1x, -f1y
                a1x = f1x / obj.m
                a1y = f1y / obj.m
                a2x = f2x / new_obj.m
                a2y = f2y / new_obj.m
                obj.vx += a1x * dt
                obj.vy += a1y * dt
                new_obj.vx += a2x * dt
                new_obj.vy += a2y * dt

        # wall collisions
        if obj.y <= obj.r:
            wall_top.x = obj.x
            Fx, Fy = obj.force_balls(wall_top)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
        elif obj.y >= height - obj.r:
            wall_down.x = obj.x
            Fx, Fy = obj.force_balls(wall_down)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
        if obj.x <= obj.r:
            wall_left.y = obj.y
            Fx, Fy = obj.force_balls(wall_left)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt
        elif obj.x >= width - obj.r:
            wall_right.y = obj.y
            Fx, Fy = obj.force_balls(wall_right)
            ax = Fx / obj.m
            ay = Fy / obj.m
            obj.vx += ax * dt
            obj.vy += ay * dt

        obj.update()  # update position of the balls
    sc.fill(white)  # clear the screen
    # re-draw the particles
    for obj in ball_list:
        obj.draw_ball()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == K_q:
                cont = False
        if event.type == QUIT:
            cont = False
pygame.quit()
