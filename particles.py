from math import *
import pygame as pg
from random import uniform

puff_img = pg.transform.scale(pg.image.load("puff.png"),(150,150))

#Allpool on tehtud selle põhjalt https://github.com/kidscancode/pygame_tutorials/blob/master/examples/particle%20demo.py
#Moditud vastavalt vajadusele
class Particle(pg.sprite.Sprite):
    def __init__(self, groups, image, pos, scale=1, lifetime=500, fade_start=10):
        pg.sprite.Sprite.__init__(self, groups)
        self.scale = scale
        self.image = pg.transform.scale_by(image.copy(),self.scale)
        self.pos = pg.Vector2(pos)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.lifetime = lifetime
        self.age = 0
        self.fade_start = fade_start

    def update(self, dt):
        """Kutsume välja funktsioonid spraidi manipuleerimiseks ja uuendame selle vanust"""
        self.shrink()
        self.fade()
        self.rect.center = self.pos
        self.age += dt * 1000
        if self.age > self.lifetime:
            self.kill()

    def shrink(self):
        """Pilve suurus ajas kasvab"""
        if self.age > self.fade_start:
            try:
                ratio = (self.age - self.fade_start) / (self.lifetime - self.fade_start)
            except ZeroDivisionError:
                ratio = 1
            if ratio > 1:
                ratio = 1
            self.image = pg.transform.scale_by(puff_img.copy(),ratio*self.scale)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def fade(self):
        """Pilve läbipaistvus ajas väheneb"""
        if self.age > self.fade_start:
            try:
                ratio = (self.age - self.fade_start) / (self.lifetime - self.fade_start)
            except ZeroDivisionError:
                ratio = 1
            if ratio > 1:
                ratio = 1
            mask = int(255 * (1 - ratio))
            self.image.fill([0,0,0,mask], special_flags=pg.BLEND_RGBA_MIN)

all_sprites = pg.sprite.Group()

def particles_initalize():
    #Tagastab sprite grupi, kuhu see programm hakkab sprite sisse toppima kui kutsutakse välja alljärgnev funktsioon
    return (all_sprites)

def puff(surf, pos, scale):
    Particle(all_sprites, puff_img, pos, scale)
