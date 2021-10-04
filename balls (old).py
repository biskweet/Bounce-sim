import pygame as pg
# from pygame import gfxdraw as gfxd
from pygame.locals import QUIT
import random as r
import matplotlib.pyplot as plt
import time

pg.init()
pg.mixer.init()
WINDOWS_WIDTH = 1280
WINDOWS_HEIGHT = 720
TOTAL_INIT = 0
FPS = 60
NUM_OBJ = 200
FONT = pg.font.SysFont("JetBrains Mono", 20)
SOUNDS = (pg.mixer.Sound("pop1.mp3"),
          pg.mixer.Sound("pop2.mp3"))


class Obj:
    def __init__(self, x, y, radius, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color

    def __str__(self):
        return "Coordinates: " + str((self.x, self.y)) + " displacement: " + str((self.dx, self.dy))


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = FONT.render(fps, 0, 0)
    return fps_text, fps


def distance(obj1, obj2):
    return ((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)**0.5


def norm(vector):   
    return (vector[0]**2 + vector[1]**2)**0.5


def create_objects(NUM_OBJ, default_radius=25, radius_shift=5, speed_width=[-4, 4]):
    objects = []
    for _ in range(NUM_OBJ):

        radius = r.randint(25 - radius_shift, 25 + radius_shift)
        x = r.randint(radius, WINDOWS_WIDTH - radius)
        y = r.randint(radius, WINDOWS_HEIGHT - radius)

        dx = r.uniform(speed_width[0], speed_width[1])
        dy = r.uniform(speed_width[0], speed_width[1])

        color = [r.randint(0, 255) for _ in range(3)]

        objects.append(Obj(x, y, radius, dx, dy, color))
    return objects


beginning = time.time()                                        # Starting time
clock = pg.time.Clock()                                        # Clock for handling FPS
running = True                                                 # Game boolean
last_sound = time.time()

screen = pg.display.set_mode([WINDOWS_WIDTH, WINDOWS_HEIGHT])  # Creating window
screen.fill((240, 240, 240))                                   # Filling window w/ backroung color

objects = create_objects(NUM_OBJ, speed_width=[-8, 8], radius_shift=15)                  # Creating list of objects
movement = []
fps_hist = []

for obj in objects:                                            # Getting the normal amount of movement
    TOTAL_INIT += abs(obj.dx)
    TOTAL_INIT += abs(obj.dy)


while running:

    for event in pg.event.get():                               # Checking exit button
        if event.type == QUIT:
            running = False
            break

    else:
        total = 0
        for obj in objects:                                    # Moving each object
            obj.x += obj.dx
            obj.y += obj.dy
            total += abs(obj.dx)
            total += abs(obj.dy)

        if total > TOTAL_INIT:                                 # If too much movement, normalizing
            for obj in objects:
                obj.dx /= (total / TOTAL_INIT)
                obj.dy /= (total / TOTAL_INIT)

        # Collisions
        collided = []
        for obj1 in objects:                                   # Checking collisions below
            for obj2 in objects:
                if obj1 is obj2: continue

                if (distance(obj1, obj2) < (obj1.radius + obj2.radius)):
                   
                    vAB = (obj2.x - obj1.x, obj2.y - obj1.y)   # A is center of obj1 and B is center of obj2
                    vBA = (obj1.x - obj2.x, obj1.y - obj2.y)

                    extremity1 = (obj1.radius * (vAB[0] / norm(vAB)) + obj1.x,
                                  obj1.radius * (vAB[1] / norm(vAB)) + obj1.y)
                    extremity2 = (obj2.radius * (vBA[0] / norm(vBA)) + obj2.x,
                                  obj2.radius * (vBA[1] / norm(vBA)) + obj2.y)

                    shift = (extremity2[0] - extremity1[0], extremity2[1] - extremity1[1])

                    obj1.dx += shift[0] / (obj1.radius/obj2.radius)  # noqa: E226
                    obj1.dy += shift[1] / (obj1.radius/obj2.radius)  # noqa: E226

                    if time.time() - last_sound > 0.05:
                        r.choice(SOUNDS).play()
                        last_sound = time.time()

            if (obj1.x > WINDOWS_WIDTH - obj1.radius) or (obj1.x < obj1.radius):  # Hit a vertical wall
                obj1.dx = -obj1.dx
            if (obj1.y > WINDOWS_HEIGHT - obj1.radius) or (obj1.y < obj1.radius):  # Hit a horizontal wall
                obj1.dy = -obj1.dy


        screen.fill((240, 240, 240))
        for obj in objects:
            pg.draw.circle(screen, obj.color, (obj.x, obj.y), obj.radius)

        fps_surface, actual_fps = update_fps()
        screen.blit(fps_surface, (10, 0))
        pg.display.flip()
        #clock.tick(FPS)

        fps_hist.append(actual_fps)
        movement.append(total)

    continue

pg.quit()

plt.plot(range(len(movement)), movement)
plt.plot(range(len(fps_hist)), fps_hist)
plt.show()