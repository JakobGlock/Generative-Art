from graphics.Graphics import setup, export
from graphics.Geometry import background, color, stroke
from graphics.Geometry import Line as draw_line
from graphics.Vector import Vector as vec2
import math
import random

width, height = 1000, 1000


# Line class
class Line:
    def __init__(self, p0, d, _id):
        self.id = _id
        self.p0 = p0
        self.p1 = p0
        self.dir = d

    def draw(self):
        color(0.15, 0.15, 0.15, 1)
        draw_line(self.p0[0], self.p0[1], self.p1[0], self.p1[1])
        stroke()

    def update(self):
        self.p1 = self.p1 + self.dir

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

    def change_dir(self, a):
        current_angle = math.atan2(a[1], a[0]) * 180 / math.pi
        new_dir = random.randint(-15, 15)
        angle = math.radians(current_angle + new_dir)
        d = vec2([math.cos(angle), math.sin(angle)])
        self.dir = d

    def get_length(self):
        dist = math.hypot(self.p0[0] - self.p1[0], self.p0[1] - self.p1[1])
        return dist

    def get_direction(self):
        d = (self.p0 - self.p1) / self.get_length()
        return d * -1.0

    def get_dist_from_center(self, center):
        dist = math.hypot(self.p1[0] - center[0], self.p1[1] - center[1])
        return dist


def draw():

    background(0.95, 0.95, 0.95, 1.0)

    grid_size = 3
    border = 40
    x_step = (width-(border*2)) / float(grid_size)
    y_step = (height-(border*2)) / float(grid_size)
    x_offset = x_step / 2.0
    y_offset = y_step / 2.0

    for y in range(grid_size):
        for x in range(grid_size):
            x_pos = x_step * x + x_offset + border
            y_pos = y_step * y + y_offset + border
            my_lines = []
            num_lines = 180
            angle = (2*math.pi) / float(num_lines)
            center_x = width / 2.0
            center_y = height / 2.0
            center = vec2([x_pos, y_pos])
            circle_size = (x_step / 2.0) - 10

            order = []
            for i in range(num_lines):
                order.append(i)

                random.shuffle(order)

            for i in range(num_lines):
                index = order[i]
                pos = vec2([
                    (math.cos(angle*index) * (circle_size-0.1))+center[0],
                    (math.sin(angle*index) * (circle_size-0.1))+center[1]
                ])
                dir = (pos - vec2([center_x, center_y])) * -1.0
                my_lines.append(Line(pos, dir, i))
                my_lines[i].change_dir(dir)

                while my_lines[i].get_dist_from_center(center) < circle_size:
                    my_lines[i].update()

                    stop_drawing = False
                    for line in my_lines:
                        if line.id != my_lines[i].id:
                            if my_lines[i].intersect(line.p0, line.p1):
                                stop_drawing = True
                                break

                    if stop_drawing:
                        break

            for line in my_lines:
                if line.get_length() > 0:
                    line.draw()


def main():
    setup(width, height)
    draw()
    export()


if __name__ == '__main__':
    main()
