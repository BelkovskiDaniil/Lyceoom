import sys
from gamer import Gamer
from sprites import *
from r_c import walls_with_ray_cast
from malen import Malen
from interaction import Interaction


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
monitor = pygame.display.set_mode((WIDTH, HEIGHT))
mon_map = pygame.Surface(MAP_RES)
pygame.mouse.set_visible(False)
timer = pygame.time.Clock()
sprites = Sprites()
gamer = Gamer(sprites)
malen = Malen(monitor, mon_map, gamer)
interaction = Interaction(gamer, sprites, malen)

while True:
    gamer.movement()
    malen.bg(gamer.angle)
    walls, wall_shot = walls_with_ray_cast(gamer, malen.texture)
    malen.world(walls + [obj.object_locate(gamer, walls) for obj in sprites.list_of_sprites])
    malen.fps(timer)
    malen.mini_map()
    malen.player_weapon_shotgun([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects()
    interaction.npc_action()

    pygame.display.flip()
    timer.tick(FPS)