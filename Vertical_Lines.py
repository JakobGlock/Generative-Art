from graphics.Graphics import setup, export
from graphics.Geometry import background, color, stroke
from graphics.Geometry import Line as draw_line
from graphics.Vector import Vector as vec2
import math
import random
import numpy as np

# Some variables
width, height = 1000, 1000


class Line:
    def __init__(self, p0, dir, id):
        self.id = id
        self.p0 = p0
        self.p1 = p0
        self.dir = dir
        self.intersect = vec2([0.0, 0.0])
        self.count = 0

    def draw(self):
        color(0.0, 0.0, 0.0, 1.0)
        draw_line(self.p0[0], self.p0[1], self.p1[0], self.p1[1])
        stroke()

    def extend_line(self):
        self.p1 = self.p1 + self.dir

    def change_dir(self):
        self.count = self.count + 1

        if self.count % 40 == 0:
            angle = math.radians(random.randint(45, 135))
            dir = vec2([math.sin(angle), math.cos(angle)])
            self.dir = dir
            return True
        else:
            return False

    def edges(self):
        if self.p1[0] >= width or self.p1[0] < 0 or \
                self.p1[1] < 0 or self.p1[1] >= height-50:
            return True

    def line_intersect(self, p2, p3):
        A1 = self.p1[1] - self.p0[1]
        B1 = self.p0[0] - self.p1[0]
        C1 = A1 * self.p0[0] + B1 * self.p0[1]
        A2 = p3[1] - p2[1]
        B2 = p2[0] - p3[0]
        C2 = A2 * p2[0] + B2 * p2[1]
        denom = A1 * B2 - A2 * B1

        if denom == 0:
            return False

        intersect_x = (B2 * C1 - B1 * C2) / denom
        intersect_y = (A1 * C2 - A2 * C1) / denom

        rx0 = (intersect_x - self.p0[0]) / (self.p1[0] - self.p0[0])
        ry0 = (intersect_y - self.p0[1]) / (self.p1[1] - self.p0[1])
        rx1 = (intersect_x - p2[0]) / (p3[0] - p2[0])
        ry1 = (intersect_y - p2[1]) / (p3[1] - p2[1])

        if(((rx0 >= 0 and rx0 <= 1) or (ry0 >= 0 and ry0 <= 1)) and \
                ((rx1 >= 0 and rx1 <= 1) or (ry1 >= 0 and ry1 <= 1))):
            self.intersect = vec2([intersect_x, intersect_y])
            return True
        else:
            return False

    def get_intersect(self):
        return self.intersect

    def get_closest_point(self, p):
        a = np.linalg.norm(self.p0-p)
        b = np.linalg.norm(self.p1-p)

        if a <= b:
            self.p0 = p
        else:
            self.p1 = p


def get_direction():
    num_angles = 2
    r = int(random.uniform(0, num_angles))
    angle_step = [0, 45]

    for i in range(num_angles):
        if i == r:
            angle = math.radians(angle_step[i])

    dirs = vec2([math.sin(angle), math.cos(angle)])
    return dirs


def draw():
    background(0.95, 0.95, 0.95, 1.0)

    num_walkers = random.randint(100, 200)
    walkers = []
    x_step = float((width-100)) / num_walkers
    amt = random.uniform(0.075, 0.15)
    amt_step = random.randint(15, 80)
    start_dist = random.randint(10, 150)

    index = 0
    count = 0
    for i in range(num_walkers):
        x = float((x_step * i) + 50.0)
        pos = vec2([float(x), float(50.0)])
        angle = math.radians(0)
        dirs = vec2([math.sin(angle), math.cos(angle)])
        walkers.append(Line(pos, dirs, i))

        walk = True
        while walk:
            if count % amt_step == 0:
                r = random.uniform(0, 1)
                if r < amt and walkers[index].p0[1] > start_dist:
                    dirs = get_direction()
                    walkers.append(Line(walkers[index].p1, dirs, i))
                    index = index + 1
                else:
                    angle = math.radians(0)
                    dirs = vec2([math.sin(angle), math.cos(angle)])
                    walkers.append(Line(walkers[index].p1, dirs, i))
                    index = index + 1

            walkers[index].extend_line()

            hit_line = False
            for w in walkers:
                if walkers[index].id != w.id:
                    intersect = walkers[index].line_intersect(w.p0, w.p1)
                    if intersect:
                        hit_line = True

            hit_edge = walkers[index].edges()
            if hit_edge or hit_line:
                walk = False

            count = count + 1
        index = index + 1

    for walker in walkers:
        walker.draw()


def main():
    setup(width, height)
    draw()
    export()


# Call the main function
if __name__ == '__main__':
    main()
