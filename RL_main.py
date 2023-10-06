# Nikhil Chalisgaonkar Boids
from p5 import *
import numpy as np

# Global Variables
sc_width = 1000
sc_height = 1000
vel_factor = 1
acc_factor = 1

num_boids = 20


class Boid():
    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        vel = (np.random.rand(2) - 0.5) * vel_factor
        self.velocity = Vector(*vel)
        acc = (np.random.rand(2) - 0.5) * acc_factor
        self.acceleration = Vector(*acc)

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    def show(self):
        p5.stroke(255)
        p5.ellipse(self.position.x, self.position.y, 20, 20)



boid_array = []


for i in range(num_boids):
    p_x = np.random.rand() - 0.5
    p_y = np.random.rand() - 0.5
    boid_array.append(Boid(p_x, p_y, sc_  width, sc_height))


def setup():
    size(sc_width, sc_height)

    for boid in boid_array:
        boid.show()


def draw():
    background(255)
    stroke(0)

run()


