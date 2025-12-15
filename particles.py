from math import *
import pygame as pg
from random import uniform

puff_img = pg.transform.scale(pg.image.load("puff.png"),(150,150))

class Particle(pg.sprite.Sprite):
    def __init__(self, groups, image, pos, lifetime=500, speed_max=50, speed_min=10, fade_start=1):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = image.copy()
        self.pos = pg.Vector2(pos)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = pg.Vector2(uniform(speed_min, speed_max), 0).rotate(uniform(0, 360))
        self.lifetime = lifetime
        self.age = 0
        self.fade_start = fade_start

    def update(self, dt):
        self.shrink()
        self.fade()
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.age += dt * 1000
        if self.age > self.lifetime:
            self.kill()

    def shrink(self):
        if self.age > self.fade_start:
            try:
                ratio = (self.age - self.fade_start) / (self.lifetime - self.fade_start)
            except ZeroDivisionError:
                ratio = 1
            if ratio > 1:
                ratio = 1
            scale = 1 - ratio
            self.image = pg.transform.rotozoom(puff_img.copy(), 0, ratio)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def fade(self):
        if self.age > self.fade_start:
            try:
                ratio = (self.age - self.fade_start) / (self.lifetime - self.fade_start)
            except ZeroDivisionError:
                ratio = .5
            if ratio > .5:
                ratio = .5
            mask = int(255 * (1 - ratio))
            self.image.fill([mask, mask, mask], special_flags=pg.BLEND_RGBA_MIN)

all_sprites = pg.sprite.Group()
def particles_initalize():
    return (all_sprites)

def puff(surf, pos, radius, scale):
    Particle(all_sprites, puff_img, pos)