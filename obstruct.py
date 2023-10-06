import pygame as pg
import numpy as np


class Obstruct(pg.sprite.Sprite):
    radius = 40
    image = pg.Surface((2*radius, 2*radius), pg.SRCALPHA)
    pg.draw.circle(image, (200, 0, 0), (radius, radius), radius)

    def __init__(self, x, y):
        super().__init__()
        self.pos = pg.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.radius = 40
