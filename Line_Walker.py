from graphics.Graphics import setup, export
from graphics.Geometry import Line, background, color, stroke
from graphics.Vector import Vector as vec2
import math
import random

#############################
# This script is a bit slow #
#############################

# Variables
width, height = 1000, 1000
center_x, center_y = width/2.0, height/2.0
border = 20


# Line Class
class Line(Line):
    def __init__(self, x1, y1, x2, y2, id, dir, angle, connect):
        super().__init__(x1, y1, x2, y2)
        self.p1 = vec2([x1, y1])
        self.id = id
        self.dir = dir
        self.angle = angle
        self.connect = connect

    def update(self):
        self.p1 = self.p1 + self.dir

    def change_dir(self, a):
        current_angle = math.atan2(a[1], a[0]) * 180 / math.pi
        new_dir = 90
        b = random.randint(0, 2)
        if b == 0:
            new_dir = 0
        elif b == 1:
            new_dir = 22.5 / 2.0
        else:
            new_dir = -(22.5 / 2.0)
        angle = math.radians(current_angle + new_dir)
        dir = vec2([math.cos(angle), math.sin(angle)])
        self.dir = dir

    def edges(self):
        if self.p1[0] >= width-border or self.p1[0] < border or self.p1[1] < border or self.p1[1] >= height-border:
            return True

    def intersect(self, p2, p3):
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

        if(((rx0 >= 0 and rx0 <= 1) or (ry0 >= 0 and ry0 <= 1)) and ((rx1 >= 0 and rx1 <= 1) or (ry1 >= 0 and ry1 <= 1))):
            return True
        else:
            return False


# Main function
def draw():
    background(0.95, 0.95, 0.95, 1.0)
    color(0, 0, 0, 1)

    walkers = []
    index = 0
    angle = (math.pi*2) / 90.0
    pos = vec2([100, 100])
    dir = vec2([1, 1])
    x, y = pos[0], pos[1]
    walkers.append(Line(x, y, x, y, 0, dir, angle * 180.0 / math.pi, -1))
    line_length = 20
    depth = -1

    for i in range(3000):
        if i != 0:
            if stop_drawing is True:
                connect = random.randint(0, i-1)
                pos = walkers[connect].get_lerp(random.uniform(0.25, 0.75))
                dist = math.hypot(
                        walkers[i-1].p0[0] - center_x,
                        walkers[i-1].p0[1] - center_y
                )
                c = vec2([center_x, center_y])
                dir = ((walkers[i-1].p0 - c) / dist) * -1.0
                x, y = pos[0], pos[1]
                walkers.append(Line(x, y, x, y, i, dir, angle * 180.0 / math.pi, connect))
                walkers[i].change_dir(walkers[i].dir)
                line_length = 10
                index = index + 1
            else:
                pos = walkers[i-1].p1
                dir = walkers[i-1].dir
                x, y = pos[0], pos[1]
                walkers.append(Line(x, y, x, y, i, dir, angle * 180.0 / math.pi, -1))
                walkers[i].change_dir(walkers[i-1].dir)

        if index > 400:
            break

        stop_drawing = False

        while walkers[i].get_length() < line_length:
            walkers[i].update()

            for w in walkers:
                if walkers[i].id != w.id and walkers[i-1].id != w.id and walkers[i].connect != w.id:
                    if walkers[i].intersect(w.p0, w.p1) or walkers[i].edges():
                        stop_drawing = True
                        break

            if stop_drawing:
                break

        walkers[i].draw()
        stroke()


def main():
    setup(width, height)
    draw()
    export()


if __name__ == '__main__':
    main()
