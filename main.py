import pygame
import sys
from parameters import *
from gamer import Gamer
from sprites import *
from r_c import ray_casting
from malen import Malen


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
monitor = pygame.display.set_mode((WIDTH, HEIGHT))
mon_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))

sprite = Sprite()
timer = pygame.time.Clock()
gamer = Gamer()
malen = Malen(monitor, mon_map, gamer)

while True:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            terminate()
    gamer.movement()
    monitor.fill(BLACK)
    malen.bg(gamer.angle)
    walls = ray_casting(gamer, malen.texture)
    malen.world(walls + [obj.object_locate(gamer, walls) for obj in sprite.list_of_objects])
    malen.fps(timer)
    malen.mini_map(gamer)

    pygame.display.flip()
    timer.tick(FPS)
