import pygame as pg
import sys
import numpy as np
from boid import Boid
from obstruct import Obstruct

# Setup
pg.init()
clock = pg.time.Clock()
LEFT = 1
RIGHT = 3


# Game screen
sc_width = 1000
sc_height = 1000
sc = pg.display.set_mode((sc_width, sc_height))
dt = 10
num_boids = 50
boid_group = pg.sprite.Group()
obstruct_group = pg.sprite.Group()

# Initialising all the boidskl
for i in range(num_boids):
    p_x = np.random.rand() * sc_width
    p_y = np.random.rand() * sc_height

    boid = Boid(p_x, p_y, sc_width, sc_height)
    boid_group.add(boid)

go_to_mouse = False
# Main loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT and event.type != pg.K_c:
            (p_x, p_y) = pg.mouse.get_pos()
            boid = Boid(p_x, p_y, sc_width, sc_height)
            boid_group.add(boid)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == RIGHT:
            (p_x, p_y) = pg.mouse.get_pos()
            obstruct = Obstruct(p_x, p_y)
            obstruct_group.add(obstruct)

        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            go_to_mouse = not go_to_mouse

        if event.type == pg.KEYDOWN and event.key == pg.K_o:
            boid_group = pg.sprite.Group()
            obstruct_group = pg.sprite.Group()

        if event.type == pg.KEYDOWN and event.key == pg.K_x:
            obstruct_group = pg.sprite.Group()

    pg.display.flip()
    sc.fill((0, 0, 0))
    for boid in boid_group:
        boid.move()
        boid.wrap()
        m_p = pg.mouse.get_pos()
        boid.apply_behaviour(boid_group, obstruct_group, m_p, go_to_mouse)
    boid_group.draw(sc)
    obstruct_group.draw(sc)
    clock.tick(10)
