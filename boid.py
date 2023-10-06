import pygame as pg
import numpy as np

class Boid(pg.sprite.Sprite):
    image = pg.Surface((20, 20), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(20, 10), (0, 0), (4, 10), (0, 20)])

    def __init__(self, x, y, width, height):
        super().__init__()
        self.pos = pg.Vector2(x, y)
        dx = (np.random.rand() - 0.5) * 2
        dy = (np.random.rand() - 0.5) * 2
        ddx = (np.random.rand() - 0.5) * 2
        ddy = (np.random.rand() - 0.5) * 2

        self.vel = pg.Vector2(dx, dy)
        self.acc = pg.Vector2(ddx, ddy)
        self.rect = self.image.get_rect(center=self.pos)
        _, orient = self.vel.as_polar()
        self.image = pg.transform.rotate(Boid .image, -orient)
        self.sc_width = width
        self.sc_height = height
        self.perception_r = 150
        self.max_speed = 10
        self.max_acc = 1.5

    def move(self):
        self.pos += self.vel
        self.vel += self.acc
        _, orient = self.vel.as_polar()
        self.image = pg.transform.rotate(Boid.image, -orient)
        self.rect.center = self.pos
        if np.linalg.norm(self.vel) > self.max_speed:
            self.vel = self.vel / np.linalg.norm(self.vel) * self.max_speed

    def wrap(self):
        if self.pos.x < 0:
            self.pos.x += self.sc_width
        elif self.pos.x > self.sc_width:
            self.pos.x -= self.sc_width

        if self.pos.y < 0:
            self.pos.y += self.sc_height
        elif self.pos.y > self.sc_height:
            self.pos.y -= self.sc_height

    def align(self, boid_group):
        steering = pg.Vector2(*np.zeros(2))
        avg_vel = pg.Vector2(*np.zeros(2))
        num_neighbours = 0

        for boid in boid_group:
            if self.perception_r > np.linalg.norm(boid.pos - self.pos) > 0:
                dist = np.linalg.norm(boid.pos - self.pos)
                avg_vel += boid.vel / dist
                num_neighbours += 1

            if num_neighbours > 1:
                avg_vel /= num_neighbours
                avg_vel = pg.Vector2(*avg_vel)
                avg_vel = (avg_vel/np.linalg.norm(avg_vel)) * self.max_speed
                steering = (avg_vel - self.vel)

        return steering * 0.3

    def cohesion(self, boid_group):
        steering = pg.Vector2(*np.zeros(2))
        c_o_m = pg.Vector2(*np.zeros(2))
        num_neighbours = 0

        for boid in boid_group:
            if np.linalg.norm(boid.pos - self.pos) < self.perception_r:
                c_o_m += boid.pos
                num_neighbours += 1

        if num_neighbours > 1:
            c_o_m /= num_neighbours
            c_o_m = pg.Vector2(*c_o_m)
            vel_to_com = c_o_m - self.pos
            if np.linalg.norm(vel_to_com) > 0:
                vel_to_com = (vel_to_com / np.linalg.norm(vel_to_com)) * self.max_speed
            steering = vel_to_com - self.vel
            if np.linalg.norm(steering) > self.max_acc:
                steering = (steering / np.linalg.norm(steering)) * self.max_acc

        return steering * 0.3

    def separation(self, boid_group):
        steering = pg.Vector2(*np.zeros(2))
        avg_vec = pg.Vector2(*np.zeros(2))
        num_neighbours = 0

        for boid in boid_group:
            distance = np.linalg.norm(boid.pos - self.pos)
            if self.pos != boid.pos and distance < self.perception_r:
                diff = self.pos - boid.pos
                diff = (3*diff)/distance

                avg_vec += diff
                num_neighbours += 1

        if num_neighbours > 0:
            avg_vec /= num_neighbours
            avg_vec = pg.Vector2(*avg_vec)
            if np.linalg.norm(steering) > 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed

            steering1 = avg_vec - self.vel

            uv1 = avg_vec / np.linalg.norm(avg_vec)
            uv2 = self.vel / np.linalg.norm(self.vel)
            dot = uv1[0] * -uv2[1] + uv1[1] * uv2[0]

            if dot > 0:  # uv_2 on right side of uv_1
                steering = pg.Vector2(steering1[1], -steering1[0])
            elif dot < 0:  # uv_2 on left side of uv_1
                steering = pg.Vector2(-steering1[1], steering1[0])
            else:
                steering = pg.Vector2(steering1[1], -steering1[0])

            # steering = avg_vec - self.vel
            if np.linalg.norm(steering) > self.max_acc:
                steering = (steering / np.linalg.norm(steering)) * self.max_acc
            '''
            avg_vec /= num_neighbours
            avg_vec = pg.Vector2(*avg_vec)
            if np.linalg.norm(steering) > 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.vel
            if np.linalg.norm(steering) > self.max_acc:
                steering = (steering / np.linalg.norm(steering)) * self.max_acc
            '''
        return steering * 0.4


    def avoid_obstruct(self, obstruct_group):
        steering = pg.Vector2(*np.zeros(2))
        avg_vec = pg.Vector2(*np.zeros(2))
        num_neighbours = 0

        for obstruct in obstruct_group:
            distance = np.linalg.norm(obstruct.pos - self.pos)
            if self.pos != obstruct.pos and (distance - obstruct.radius) < self.perception_r/2:
                diff = self.pos - obstruct.pos
                diff = ((6 * diff) / (distance - obstruct.radius/2))*pow((np.linalg.norm(diff)),4)

                avg_vec += diff
                num_neighbours += 1

        if num_neighbours > 0:
            avg_vec /= num_neighbours
            avg_vec = pg.Vector2(*avg_vec)
            if np.linalg.norm(steering) > 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed

            steering1 = avg_vec - self.vel

            uv1 = avg_vec / np.linalg.norm(avg_vec)
            uv2 = self.vel / np.linalg.norm(self.vel)
            dot = uv1[0]* -uv2[1] + uv1[1]*uv2[0]

            if dot > 0: #uv_2 on right side of uv_1
                steering = pg.Vector2(steering1[1], -steering1[0])
            elif dot < 0: #uv_2 on left side of uv_1
                steering = pg.Vector2(-steering1[1], steering1[0])
            else:
                steering = pg.Vector2(steering1[1], -steering1[0])


            #steering = avg_vec - self.vel
            if np.linalg.norm(steering) > self.max_acc:
                steering = (steering / np.linalg.norm(steering)) * self.max_acc

        return steering*2

    def go_to_mouse(self, m_p, go_to_mouse):
        steering = pg.Vector2(*np.zeros(2))
        if go_to_mouse:
            mouse_pos = pg.Vector2(*np.zeros(2))

            mouse_pos = pg.Vector2(*m_p)
            vel_to_mouse = mouse_pos - self.pos
            if np.linalg.norm(vel_to_mouse) > 0:
                vel_to_com = (vel_to_mouse / np.linalg.norm(vel_to_mouse)) * self.max_speed
            steering = vel_to_mouse - self.vel
            if np.linalg.norm(steering) > self.max_acc:
                steering = (steering / np.linalg.norm(steering)) * self.max_acc

        return steering

    '''
    def avoid_walls(self):
        steering = pg.Vector2(*np.zeros(2))

        if self.pos.x < self.perception_r:
            distance = self.pos.x
            vec = pg.Vector2(-5/distance, 0)
            steering = vec - self.vel


        return steering
    '''

    def apply_behaviour(self, boid_group, obstruct_group, m_p, go_to_mouse):
        alignment = self.align(boid_group)
        cohesion = self.cohesion(boid_group)
        separation = self.separation(boid_group)
        avoid_obstruct = self.avoid_obstruct(obstruct_group)
        go_to_mouse = self.go_to_mouse(m_p, go_to_mouse)
        #avoid = self.avoid_walls()

        self.acc += alignment
        self.acc += cohesion
        self.acc += separation
        self.acc += avoid_obstruct
        self.acc += go_to_mouse
        #self.acc += avoid
        self.acc *= 0.75