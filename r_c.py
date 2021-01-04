import pygame
from parameters import *
from map import txt_map, H_WORLD, W_WORLD
#from new_map import txt_map, H_WORLD, W_WORLD



def mapping(a, b):
    return int((a // CELL) * CELL), int((b // CELL) * CELL)


def ray_casting(gamer, textures):
    walls = []
    ox, oy = gamer.pos
    texture_v, texture_h = 1, 1
    xm, ym = mapping(ox, oy)
    view_angle = gamer.angle - H_FOV
    for ray in range(N_RAYS):
        sin_a = math.sin(view_angle)
        cos_a = math.cos(view_angle)

        x, dx = (xm + CELL, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, W_WORLD, CELL):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in txt_map:
                texture_v = txt_map[tile_v]
                break
            x += dx * CELL

        y, dy = (ym + CELL, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, H_WORLD, CELL):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in txt_map:
                texture_h = txt_map[tile_h]
                break
            y += dy * CELL

        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % CELL
        depth *= math.cos(gamer.angle - view_angle)
        depth = max(depth, 0.00001)
        hight = min((PROJ_C / depth), P_HEIGHT)


        wall_c = textures[texture].subsurface(offset * T_SCALE, 0, T_SCALE, T_H)
        wall_c = pygame.transform.scale(wall_c, (int(SCALE), int(hight)))
        walls_pos = (ray * SCALE, H_HEIGHT - hight // 2)

        walls.append((depth, wall_c, walls_pos))
        view_angle += DELTA_ANGLE
    return walls
