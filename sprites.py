from parameters import *
import pygame
import os
import math
from collections import deque


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Sprites:
    def __init__(self):
        self.new_types = {
            'fire': {
                'way': pygame.image.load('data/sprites/fire/base/3.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque([pygame.image.load(f'data/sprites/fire/action/{i}.png').convert_alpha()
                                    for i in range(1, 16)]),
                'animation_dist': 800,
                'animation_speed': 10
            },
            'sosademon': {
                'way': [pygame.image.load(f'data/sprites/sosademon/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0,
                'scale': 1,
                'animation': deque([pygame.image.load(f'data/sprites/sosademon/action/{i}.png').convert_alpha()
                                    for i in range(6)]),
                'animation_dist': 150,
                'animation_speed': 5
            },
            'barrel': {
                'way': pygame.image.load('data/sprites/barrel/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 1.8,
                'scale': 0.4,
                'animation': None,
                'animation_dist': 150,
                'animation_speed': 5
            }
        }

        self.list_of_sprites = [AllSprites(self.new_types['fire'], (7.1, 2.1)),
                                AllSprites(self.new_types['fire'], (7.1, 4.1)),
                                AllSprites(self.new_types['fire'], (5.1, 2.1)),
                                AllSprites(self.new_types['fire'], (10.1, 2.1)),
                                AllSprites(self.new_types['fire'], (7.1, 5.1)),
                                AllSprites(self.new_types['barrel'], (8.1, 9.1)),
                                AllSprites(self.new_types['sosademon'], (5.51, 12.43))]


class AllSprites:
    def __init__(self, parameters,  pos):
        self.obj = parameters['way']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.pos = self.x, self.y = pos[0] * CELL, pos[1] * CELL

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}

    def object_locate(self, gamer, walls):
        fake_walls0 = [walls[0] for i in range(100)]
        fake_walls1 = [walls[-1] for i in range(100)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - gamer.x, self.y - gamer.y
        dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        betta = math.atan2(dy, dx)
        gamma = betta - gamer.angle
        if dx > 0 and 180 <= math.degrees(gamer.angle) <= 360 or dx < 0 and dy < 0:
            gamma += ZWEI_PI
        d_rays = int(gamma / DELTA_ANGLE)
        current_ray = C_RAY + d_rays
        dist_to_sprite *= math.cos(H_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and dist_to_sprite > 30:
            p_height = min(int(PROJ_C / dist_to_sprite * self.scale), D_HEIGHT)
            h_p_height = p_height // 2
            shift = h_p_height * self.shift

            if self.viewing_angles:
                if betta < 0:
                    betta += ZWEI_PI
                betta = 360 - int(math.degrees(betta))

                for angles in self.sprite_angles:
                    if betta in angles:
                        self.obj = self.sprite_positions[angles]
                        break

            sprite_object = self.obj
            if self.animation and dist_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
            sprite_pos = (current_ray * SCALE - h_p_height, H_HEIGHT - h_p_height + shift)
            sprite = pygame.transform.scale(sprite_object, (p_height, p_height))
            return (dist_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
